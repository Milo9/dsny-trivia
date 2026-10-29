// Offline practice only. Firestore and all cross-origin requests stay network-only.
const CACHE = 'disney-practice-1.39';
const CORE = ['./', 'index.html', 'style.css?v=1.39', 'bootstrap.js?v=1.39',
  'game-logic.js?v=1.39', 'data-logic.js?v=1.39', 'storage.js?v=1.39', 'app.js?v=1.39',
  'questions/manifest.json', 'movies.json', 'manifest.json', 'icons/icon-192.png', 'icons/icon-512.png'];
self.addEventListener('install', event => event.waitUntil((async () => {
  const cache = await caches.open(CACHE);
  await cache.addAll(CORE);
  const manifest = await (await cache.match('questions/manifest.json')).json();
  await cache.addAll(manifest.shards.concat(manifest.retired ? [manifest.retired] : []));
  await self.skipWaiting();
})()));
self.addEventListener('activate', event => event.waitUntil((async () => {
  for (const key of await caches.keys()) if (key.startsWith('disney-practice-') && key !== CACHE) await caches.delete(key);
  await self.clients.claim();
})()));
self.addEventListener('fetch', event => {
  const request = event.request, url = new URL(request.url);
  if (request.method !== 'GET' || url.origin !== self.location.origin || url.pathname.endsWith('/review.html')) return;
  event.respondWith((async () => {
    const cache = await caches.open(CACHE);
    try {
      const response = await fetch(request);
      if (response.ok && !url.searchParams.has('t')) await cache.put(request, response.clone());
      return response;
    } catch (error) {
      // Update probes must not mistake cached HTML for a freshly deployed build.
      if (url.searchParams.has('t')) throw error;
      const cached = await cache.match(request);
      if (cached) return cached;
      if (request.mode === 'navigate') return (await cache.match('index.html')) || Response.error();
      throw error;
    }
  })());
});
