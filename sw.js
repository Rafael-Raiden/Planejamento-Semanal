/* Service worker do Planejamento TI.
   Guarda a "casca" do app para abrir rápido e funcionar sem internet no modo local.
   Os dados NÃO passam por aqui: ficam no navegador (localStorage) ou na planilha do Google.
   Ao publicar uma mudança no app, aumente VERSAO para os celulares trocarem o cache. */
const VERSAO = 'pti-v1';
const CASCA = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icons/favicon.svg',
  './icons/favicon-32.png',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/apple-touch-icon.png'
];

self.addEventListener('install', (ev) => {
  ev.waitUntil(caches.open(VERSAO).then((c) => c.addAll(CASCA)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (ev) => {
  ev.waitUntil(
    caches.keys()
      .then((nomes) => Promise.all(nomes.filter((n) => n !== VERSAO).map((n) => caches.delete(n))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (ev) => {
  const req = ev.request;
  const url = new URL(req.url);
  /* Só arquivos do próprio site. Planilha (script.google.com) e fontes do Google seguem direto pela rede. */
  if (req.method !== 'GET' || url.origin !== self.location.origin) { return; }

  /* Página: rede primeiro, para sempre pegar a versão nova; sem internet, usa a cópia guardada. */
  if (req.mode === 'navigate') {
    ev.respondWith(
      fetch(req)
        .then((r) => {
          if (r.ok) { const copia = r.clone(); caches.open(VERSAO).then((c) => c.put('./index.html', copia)); }
          return r;
        })
        .catch(() => caches.match('./index.html'))
    );
    return;
  }

  /* Ícones e manifesto: cópia guardada primeiro, rede como reserva. */
  ev.respondWith(caches.match(req).then((guardado) => guardado || fetch(req)));
});
