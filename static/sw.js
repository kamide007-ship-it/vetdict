// VetDict Service Worker — offline support & caching
const CACHE_NAME = 'vetdict-v39';
const STATIC_ASSETS = [
  '/',
  '/static/favicon.svg',
  '/static/manifest.json',
];

// Install: cache static assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting();
});

// Activate: clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Fetch: network-first for API, cache-first for static assets
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // API requests: network with offline fallback
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(event.request).catch(() =>
        new Response(JSON.stringify({ error: 'offline', message: 'ネットワークに接続できません。', message_en: 'Network unavailable. Please check your connection.' }), {
          status: 503,
          headers: { 'Content-Type': 'application/json' },
        })
      )
    );
    return;
  }

  // Disease pages: network-first, cache for offline
  if (url.pathname.startsWith('/diseases')) {
    event.respondWith(
      fetch(event.request).then((response) => {
        if (response && response.status === 200) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
        }
        return response;
      }).catch(() =>
        caches.match(event.request).then((cached) =>
          cached || (event.request.mode === 'navigate' ? caches.match('/') : new Response('Offline', { status: 503 }))
        )
      )
    );
    return;
  }

  // Versioned static assets (e.g. app.js?v=5.0.0): network-first to ensure fresh content
  if (url.pathname.startsWith('/static/') && url.search) {
    event.respondWith(
      fetch(event.request).then((response) => {
        if (response && response.status === 200) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
        }
        return response;
      }).catch(() =>
        caches.match(event.request).then((cached) =>
          cached || new Response('Offline', { status: 503 })
        )
      )
    );
    return;
  }

  // Static assets (no query): cache-first with background revalidation
  event.respondWith(
    caches.match(event.request).then((cached) => {
      if (cached) {
        // Revalidate in background
        fetch(event.request).then((response) => {
          if (response && response.status === 200) {
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, response));
          }
        }).catch(() => {});
        return cached;
      }
      return fetch(event.request).then((response) => {
        if (response && response.status === 200 && url.pathname.startsWith('/static/')) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
        }
        return response;
      }).catch(() =>
        // Offline fallback for navigation requests
        event.request.mode === 'navigate'
          ? caches.match('/')
          : new Response('Offline', { status: 503 })
      );
    })
  );
});
