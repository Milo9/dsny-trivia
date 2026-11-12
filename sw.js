// Offline practice only. Firestore and all cross-origin requests stay network-only.
const CACHE = 'disney-practice-1.54';
const CORE = ['./', 'index.html', 'style.css?v=1.54', 'bootstrap.js?v=1.54',
  'game-logic.js?v=1.54', 'data-logic.js?v=1.54', 'storage.js?v=1.54', 'app.js?v=1.54',
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
// Network-first, but a stalled connection (ship/hotel wifi that accepts the
// request and never answers) must not hang the app: after NETWORK_WAIT_MS the
// cached copy is served while the network request keeps running in the
// background and refreshes the cache if it eventually succeeds.
// Once a request has stalled, the next ones (the app loads its scripts in
// sequence) wait only briefly, so a stalled boot costs ~4 s rather than ~4 s per
// file. Any successful network response restores the normal wait.
const NETWORK_WAIT_MS = 4000, STALLED_WAIT_MS = 300, STALLED_FOR_MS = 30000;
let stalledUntil = 0;
self.addEventListener('fetch', event => {
  const request = event.request, url = new URL(request.url);
  if (request.method !== 'GET' || url.origin !== self.location.origin || url.pathname.endsWith('/review.html')) return;
  // Update probes (?t=) must not mistake cached HTML for a freshly deployed build.
  const probe = url.searchParams.has('t');
  const network = fetch(request).then(async response => {
    stalledUntil = 0;
    if (response.ok && !probe) await (await caches.open(CACHE)).put(request, response.clone());
    return response;
  });
  if (probe) { event.respondWith(network); return; }
  event.waitUntil(network.catch(() => {}));
  event.respondWith((async () => {
    let timer;
    const wait = Date.now() < stalledUntil ? STALLED_WAIT_MS : NETWORK_WAIT_MS;
    const stalled = new Promise((_, reject) => { timer = setTimeout(() => {
      stalledUntil = Date.now() + STALLED_FOR_MS;
      reject(new Error('stalled'));
    }, wait); });
    try {
      return await Promise.race([network, stalled]);
    } catch (error) {
      const cache = await caches.open(CACHE);
      const cached = (await cache.match(request)) || (request.mode === 'navigate' ? await cache.match('index.html') : undefined);
      if (cached) return cached;
      return network; // nothing cached: keep waiting for (or fail with) the network
    } finally {
      clearTimeout(timer);
    }
  })());
});
