"""Regression tests for the mobile "every tap is dead" boot failure (第60弾).

Root cause: iOS Safari with "Block All Cookies" (and some private-browsing
modes) throws a SecurityError on ANY localStorage access. checkAccess() touched
localStorage bare, and the whole DOMContentLoaded init ran inside a single
try/catch — so one throw silently skipped everything after it, including
setupNavigation()/setupMobileBottomNav(). Result: no bottom nav and no tab or
species handlers; tapping 薬品DB / 疾患DB / 動物種 did nothing.

Fixes under test:
1. All localStorage access in app.js goes through guarded lsGet/lsSet/lsRemove.
2. The boot is compartmentalised: each setup step runs in its own _boot() wrapper
   so one failure cannot kill navigation setup.
3. index.html inline consent scripts guard their own localStorage access.
4. sw.js serves navigations network-first (a stale cached HTML shell can no
   longer pair with a newer network-first app.js and break init), CACHE_NAME
   bumped so old caches cycle out.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
SW_JS = (ROOT / "static" / "sw.js").read_text(encoding="utf-8")
INDEX_HTML = (ROOT / "templates" / "index.html").read_text(encoding="utf-8")


class TestGuardedLocalStorage:
    def test_helpers_defined(self):
        assert "function lsGet(k){try{return window.localStorage.getItem(k);}catch(_){return null;}}" in APP_JS
        assert "function lsSet(k,v){try{window.localStorage.setItem(k,v);}catch(_){}}" in APP_JS
        assert "function lsRemove(k){try{window.localStorage.removeItem(k);}catch(_){}}" in APP_JS

    def test_no_bare_localstorage_calls_outside_helpers(self):
        # The only direct member calls allowed are the three inside the helpers.
        assert APP_JS.count("localStorage.getItem(") == 1
        assert APP_JS.count("localStorage.setItem(") == 1
        assert APP_JS.count("localStorage.removeItem(") == 1

    def test_check_access_uses_guarded_accessors(self):
        start = APP_JS.index("async function checkAccess()")
        body = APP_JS[start : start + 2000]
        assert "lsGet(" in body
        assert "localStorage.getItem(" not in body

    def test_index_html_consent_scripts_are_guarded(self):
        # Head IIFE that syncs a previously granted consent must not die on
        # blocked storage (it runs before app.js on every page load).
        head_iife = INDEX_HTML[INDEX_HTML.index("vetdict-analytics-consent") - 200 :][:400]
        assert "try{" in head_iife
        # Banner logic uses guarded accessors so the banner still shows and
        # dismisses when storage is blocked (choice simply doesn't persist).
        assert "function _consentGet()" in INDEX_HTML
        assert "function _consentSet(" in INDEX_HTML
        consent_block = INDEX_HTML[INDEX_HTML.index("function _setConsent") :]
        assert "localStorage.setItem" not in consent_block.split("</script>")[0].replace(
            "function _consentSet(v){try{localStorage.setItem('vetdict-analytics-consent',v);}catch(e){}}", ""
        )


class TestCompartmentalisedBoot:
    def test_boot_wrapper_defined(self):
        assert "function _boot(name,fn){" in APP_JS
        # Async setup steps: rejected promises are logged, not left unhandled.
        assert 'typeof r.catch==="function"' in APP_JS

    def test_critical_nav_steps_individually_wrapped(self):
        for step in [
            '_boot("setupNavigation",setupNavigation)',
            '_boot("setupMobileBottomNav",setupMobileBottomNav)',
            '_boot("dbListDelegation"',
            '_boot("hashRouting"',
            '_boot("speciesParam"',
        ]:
            assert step in APP_JS, f"missing isolated boot step: {step}"

    def test_boot_steps_are_numerous(self):
        # One monolithic try/catch had exactly zero isolation points. Keep the
        # boot split into many independently-failing steps.
        assert APP_JS.count("_boot(") >= 20

    def test_check_access_failure_is_contained(self):
        assert 'try{await checkAccess();}catch(e){debugError("boot:checkAccess",e);}' in APP_JS


class TestServiceWorkerNavigationFreshness:
    def test_cache_name_bumped(self):
        m = re.search(r"vetdict-v(\d+)", SW_JS)
        assert m and int(m.group(1)) >= 167

    def test_navigations_are_network_first(self):
        nav_idx = SW_JS.index("Navigations / the app shell ('/')")
        static_idx = SW_JS.index("cache-first with background revalidation")
        assert nav_idx < static_idx, "navigate branch must run before the cache-first static branch"
        nav_block = SW_JS[nav_idx : nav_idx + 1200]
        assert "event.request.mode === 'navigate'" in nav_block
        assert "fetch(event.request)" in nav_block
        assert ".catch(" in nav_block and "caches.match" in nav_block

    def test_root_shell_included_in_navigation_branch(self):
        nav_idx = SW_JS.index("Navigations / the app shell ('/')")
        block = SW_JS[nav_idx : nav_idx + 800]
        assert "url.pathname === '/'" in block
