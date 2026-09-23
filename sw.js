/* =====================================================================
   Constella Service Worker — Offline Course Portal & PWA Engine
   ===================================================================== */

const CACHE_NAME = 'constella-v1.0.3';

// Core application shell assets to pre-cache on install
const CORE_ASSETS = [
  './',
  './index.html',
  './courses.js',
  './favicon.svg',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  './icon-maskable-512.png',
  './apple-touch-icon.png'
];

// Pre-cache core assets
self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(CORE_ASSETS).catch((err) => {
        console.warn('[SW] Pre-cache warning:', err);
      });
    })
  );
});

// Clean up old caches on activation and claim clients immediately
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    }).then(() => self.clients.claim())
  );
});

// Network-First strategy with Cache Fallback for navigation & dynamic files
async function networkFirst(request) {
  try {
    const networkResponse = await fetch(request);
    if (networkResponse && networkResponse.status === 200) {
      const responseClone = networkResponse.clone();
      caches.open(CACHE_NAME).then((cache) => cache.put(request, responseClone));
    }
    return networkResponse;
  } catch (error) {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    // If navigation request and no cache match, return cached index.html
    if (request.mode === 'navigate') {
      const indexFallback = await caches.match('./index.html');
      if (indexFallback) return indexFallback;
    }
    throw error;
  }
}

// Cache-First strategy with Network update for static fonts and images
async function cacheFirst(request) {
  const cachedResponse = await caches.match(request);
  if (cachedResponse) {
    // Optionally revalidate in background
    fetch(request).then((networkResponse) => {
      if (networkResponse && networkResponse.status === 200) {
        caches.open(CACHE_NAME).then((cache) => cache.put(request, networkResponse));
      }
    }).catch(() => {});
    return cachedResponse;
  }

  try {
    const networkResponse = await fetch(request);
    if (networkResponse && networkResponse.status === 200) {
      const responseClone = networkResponse.clone();
      caches.open(CACHE_NAME).then((cache) => cache.put(request, responseClone));
    }
    return networkResponse;
  } catch (err) {
    return cachedResponse;
  }
}

self.addEventListener('fetch', (event) => {
  const request = event.request;
  const url = new URL(request.url);

  // Ignore non-GET requests and browser extensions
  if (request.method !== 'GET' || !url.protocol.startsWith('http')) {
    return;
  }

  // Pass-through Firebase Analytics or remote scripts without blocking
  if (url.hostname.includes('firebase') || url.hostname.includes('google-analytics')) {
    event.respondWith(
      fetch(request).catch(() => new Response('', { status: 200, statusText: 'Offline' }))
    );
    return;
  }

  // Google Fonts (Cache First)
  if (url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
    event.respondWith(cacheFirst(request));
    return;
  }

  // Navigation (HTML pages) and dynamic course definition (courses.js) -> Network First
  if (request.mode === 'navigate' || url.pathname.endsWith('courses.js') || url.pathname.endsWith('.html') || url.pathname.endsWith('/')) {
    event.respondWith(networkFirst(request));
    return;
  }

  // Static images, SVGs, icons -> Cache First
  if (/\.(svg|png|jpg|jpeg|webp|ico)$/i.test(url.pathname)) {
    event.respondWith(cacheFirst(request));
    return;
  }

  // Default: Network First with cache fallback
  event.respondWith(networkFirst(request));
});

// Listen for message events (e.g. SKIP_WAITING from client)
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
