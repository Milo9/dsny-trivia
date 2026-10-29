// Core files load independently of optional CDN scripts. Bound each CDN wait,
// so the local practice screen remains reachable on unreliable connections.
(() => {
  const version = new URL(document.currentScript.src).searchParams.get('v') || '1.39';
  const load = (src, timeout = 10000) => new Promise((resolve, reject) => {
    const script = document.createElement('script');
    const timer = setTimeout(() => { script.remove(); reject(new Error('Connection timed out.')); }, timeout);
    script.src = src;
    script.onload = () => { clearTimeout(timer); resolve(); };
    script.onerror = () => { clearTimeout(timer); reject(new Error('Could not load ' + src)); };
    document.head.appendChild(script);
  });
  globalThis.firebaseReady = load('https://www.gstatic.com/firebasejs/10.12.0/firebase-app-compat.js', 5000)
    .then(() => load('https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore-compat.js', 5000));
  globalThis.firebaseReady.catch(() => {});
  (async () => {
    for (const name of ['game-logic.js', 'data-logic.js', 'storage.js', 'app.js']) await load(name + '?v=' + version);
  })().catch(() => {
    const out = document.getElementById('user-list');
    out.replaceChildren();
    const message = document.createElement('p'); message.textContent = 'The app could not load. Check your connection and reload.';
    const retry = document.createElement('button'); retry.className = 'btn-secondary'; retry.textContent = 'Reload'; retry.onclick = () => location.reload();
    out.append(message, retry);
  });
})();
