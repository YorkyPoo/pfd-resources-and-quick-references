# mkdocs_post_build.py — generate pre-cache service worker after MkDocs build
import os
import json
from datetime import datetime, timezone

def on_post_build(config, **kwargs):
    site_dir = config["site_dir"]
    
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk(site_dir):
        # Skip the service worker itself and search index
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for f in files:
            if f.endswith(".html") and f != "sw.js":
                rel_path = os.path.relpath(os.path.join(root, f), site_dir).replace("\\", "/")
                html_files.append(f"/pfd-resources-and-quick-references/{rel_path}")
    
    html_files.sort()
    
    # Generate version stamp
    version = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    
    # Build the service worker
    urls_json = json.dumps(html_files, indent=4)
    
    sw_content = f'''// Pre-Cache Service Worker for Poquoson Fire & Rescue Protocols
// Generated: {version}
// Caches ALL protocols on first visit for full offline access

const CACHE_NAME = "pfd-protocols-v{version}";

const PRECACHE_URLS = {urls_json};

// Install: download and cache every page
self.addEventListener("install", event => {{
    console.log("[SW] Installing — caching {{PRECACHE_URLS.length}} pages...");
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {{
                // Cache in small batches to avoid overwhelming the browser
                const batchSize = 10;
                const cacheInBatches = async () => {{
                    for (let i = 0; i < PRECACHE_URLS.length; i += batchSize) {{
                        const batch = PRECACHE_URLS.slice(i, i + batchSize);
                        await Promise.all(
                            batch.map(url =>
                                cache.add(url).catch(err =>
                                    console.warn("[SW] Failed to cache:", url, err)
                                )
                            )
                        );
                        console.log(`[SW] Cached ${{Math.min(i + batchSize, PRECACHE_URLS.length)}}/${{PRECACHE_URLS.length}} pages`);
                    }}
                }};
                return cacheInBatches();
            }})
            .then(() => self.skipWaiting())
    );
}});

// Activate: clean up old caches
self.addEventListener("activate", event => {{
    console.log("[SW] Activating — cleaning old caches");
    event.waitUntil(
        caches.keys().then(cacheNames => {{
            return Promise.all(
                cacheNames
                    .filter(name => name !== CACHE_NAME)
                    .map(name => {{
                        console.log("[SW] Deleting old cache:", name);
                        return caches.delete(name);
                    }})
            );
        }}).then(() => self.clients.claim())
    );
}});

// Fetch: cache-first strategy — serve from cache, fall back to network
self.addEventListener("fetch", event => {{
    // Only handle GET requests for same-origin resources
    if (event.request.method !== "GET") return;
    
    const url = new URL(event.request.url);
    
    // Only cache same-origin HTML pages and assets
    if (url.origin !== self.location.origin) return;
    
    event.respondWith(
        caches.match(event.request).then(cachedResponse => {{
            if (cachedResponse) {{
                return cachedResponse;
            }}
            // Not in cache — fetch from network and cache for next time
            return fetch(event.request).then(response => {{
                if (response && response.status === 200) {{
                    const responseToCache = response.clone();
                    caches.open(CACHE_NAME).then(cache => {{
                        cache.put(event.request, responseToCache);
                    }});
                }}
                return response;
            }}).catch(() => {{
                // Offline and not cached — return the homepage
                return caches.match("/pfd-resources-and-quick-references/index.html");
            }});
        }})
    );
}});

console.log("[SW] Poquoson Fire & Rescue — {len(html_files)} pages ready for offline use");
'''

    # Write the service worker
    sw_path = os.path.join(site_dir, "sw.js")
    with open(sw_path, "w", encoding="utf-8") as f:
        f.write(sw_content)
    
    print(f"[post_build] Generated sw.js with {len(html_files)} pre-cached pages (version: {version})")
