const CACHE = "localintel-ai-v1";
const ASSETS = ["/", "/index.html", "/manifest.webmanifest", "/icon.svg"];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(ASSETS)));
});

self.addEventListener("fetch", (event) => {
  // Only handle GET requests. POST/PUT/DELETE/etc. bypass the service worker cache.
  if (event.request.method !== "GET") {
    return;
  }

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }

      return fetch(event.request).then((response) => {
        // Only cache successful same-origin responses
        if (!response || response.status !== 200 || response.type !== "basic") {
          return response;
        }

        // Avoid caching backend API calls to ensure data freshness
        const url = new URL(event.request.url);
        if (url.pathname.startsWith("/api/")) {
          return response;
        }

        const responseToCache = response.clone();
        caches.open(CACHE).then((cache) => {
          cache.put(event.request, responseToCache);
        });

        return response;
      }).catch(() => {
        // Fallback for network failures when completely offline
      });
    })
  );
});

