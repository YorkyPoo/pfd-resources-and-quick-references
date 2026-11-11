# mkdocs_post_build.py — generate pre-cache service worker after MkDocs build
import os
import re
import json
from datetime import datetime, timezone

def on_post_build(config, **kwargs):
    site_dir = config["site_dir"]

    # --- sitemap hygiene, derived not hardcoded ------------------------------------
    # Any built page carrying <meta name="robots" content="noindex...> is dropped from
    # sitemap.xml. Reading the rendered HTML means this can never disagree with the
    # front-matter flag that overrides/main.html turns into that tag — add a new noindex
    # page and it self-registers. (MkDocs 1.6.1 has no exclude_from_sitemap option; probed:
    # the string is absent from the installed package. A meta tag alone still leaves the URL
    # discoverable in the sitemap, which is exactly the leak this closes.)
    noindex = []
    for root, dirs, files in os.walk(site_dir):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", "assets")]
        for fn in files:
            if not fn.endswith(".html"):
                continue
            fp = os.path.join(root, fn)
            with open(fp, encoding="utf-8", errors="replace") as fh:
                head = fh.read(4000)          # the meta tag is in <head>, near the top
            if re.search(r'name="robots"[^>]*noindex', head):
                noindex.append("/" + os.path.relpath(fp, site_dir).replace("\\", "/"))

    sm = os.path.join(site_dir, "sitemap.xml")
    if noindex and os.path.exists(sm):
        with open(sm, encoding="utf-8") as fh:
            xml = fh.read()
        for url_path in noindex:
            xml = re.sub(r"<url>(?:(?!</url>).)*?" + re.escape(url_path)
                         + r"(?:(?!</url>).)*?</url>", "", xml, flags=re.S)
        with open(sm, "w", encoding="utf-8") as fh:
            fh.write(xml)
        print(f"[post_build] sitemap: dropped {len(noindex)} noindex page(s): {noindex}")

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

// Fetch: fresh-when-online, cached-when-offline
// HTML/CSS/JS/JSON: network-first (fall back to cache offline) so edits appear
// immediately; images/icons: cache-first (immutable assets).
self.addEventListener("fetch", event => {{
    if (event.request.method !== "GET") return;
    const url = new URL(event.request.url);
    if (url.origin !== self.location.origin) return;

    const isContent = event.request.mode === "navigate"
        || /\.(html?|css|js|json|webmanifest)$/i.test(url.pathname)
        || url.pathname.endsWith("/");

    if (!isContent) {{
        event.respondWith(caches.match(event.request).then(c => c || fetch(event.request)));
        return;
    }}

    event.respondWith(
        fetch(event.request).then(response => {{
            if (response && response.status === 200) {{
                const clone = response.clone();
                caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
            }}
            return response;
        }}).catch(() => caches.match(event.request).then(cached =>
            cached || (event.request.mode === "navigate"
                ? caches.match("/pfd-resources-and-quick-references/index.html")
                : Response.error())))
    );
}});
'''

    # Write the service worker
    sw_path = os.path.join(site_dir, "sw.js")
    with open(sw_path, "w", encoding="utf-8") as f:
        f.write(sw_content)
    
    print(f"[post_build] Generated sw.js with {len(html_files)} pre-cached pages (version: {version})")
