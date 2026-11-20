const CACHE = 'italiano-202611200758';
const FILES = ['./', 'index.html', 'data.json', 'manifest.webmanifest', 'icon-180.png', 'icon-512.png'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
// Only keep a download if it is really our file (plane Wi-Fi login pages must never replace the app)
async function good(path, r) {
  if (!r || !r.ok || r.redirected) return false;
  try {
    const t = await r.clone().text();
    if (path.endsWith('data.json')) { const j = JSON.parse(t); return !!(j && j.docs); }
    if (path.endsWith('/') || path.endsWith('index.html')) return t.indexOf('Italiano offline') !== -1;
    return true;
  } catch (err) { return false; }
}
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) {
    e.respondWith(caches.open(CACHE).then(c => c.match(req).then(hit => hit || fetch(req).then(r => { c.put(req, r.clone()); return r; }))).catch(() => Response.error()));
    return;
  }
  const key = (req.mode === 'navigate' || url.pathname.endsWith('/')) ? 'index.html' : req;
  // Open instantly from the saved copy; check for a newer version in the background for next time
  e.respondWith(caches.open(CACHE).then(async c => {
    const hit = await c.match(key, { ignoreSearch: true });
    const update = fetch(req, { cache: 'no-cache' }).then(async r => {
      if (await good(url.pathname, r)) await c.put(key, r.clone());
      return r;
    });
    if (hit) { try { e.waitUntil(update.catch(() => {})); } catch (err) {} return hit; }
    return update.catch(() => Response.error());
  }));
});
