import importlib
import sys

import pytest


@pytest.fixture(autouse=True)
def restore_debug_modules():
    original_modules = {
        module_name: sys.modules.get(module_name)
        for module_name in ('api.vetdict_api', 'api.showdog_api')
    }
    yield
    for module_name, module in original_modules.items():
        if module is None:
            sys.modules.pop(module_name, None)
        else:
            sys.modules[module_name] = module


@pytest.mark.parametrize("module_name", ["api.vetdict_api", "api.showdog_api"])
def test_debug_mode_defaults_to_on(module_name, monkeypatch):
    monkeypatch.delenv('FLASK_DEBUG', raising=False)
    sys.modules.pop(module_name, None)

    module = importlib.import_module(module_name)

    assert module.is_debug_mode_enabled() is True
    assert module.app.config['DEBUG'] is True


@pytest.mark.parametrize("module_name", ["api.vetdict_api", "api.showdog_api"])
def test_debug_mode_can_be_disabled_via_env(module_name, monkeypatch):
    monkeypatch.setenv('FLASK_DEBUG', '0')
    sys.modules.pop(module_name, None)

    module = importlib.import_module(module_name)

    assert module.is_debug_mode_enabled() is False
    assert module.app.config['DEBUG'] is False
