#!/usr/bin/env python3
import asyncio
import aiohttp
import xml.etree.ElementTree as ET
import argparse

# Standard sitemap namespace
SITEMAP_NAMESPACE = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
USER_AGENT = "SitemapPinger/1.0 (+https://github.com/your-repo-if-any)" # Be a good netizen

async def fetch_url_content(session, url):
    """Fetches the content of a URL (typically a sitemap)."""
    print(f"Fetching sitemap/index: {url}")
    try:
        async with session.get(url, headers={'User-Agent': USER_AGENT}, timeout=30) as response:
            response.raise_for_status()  # Raise an exception for HTTP errors
            return await response.text()
    except asyncio.TimeoutError:
        print(f"Timeout fetching {url}")
    except aiohttp.ClientError as e:
        print(f"Error fetching {url}: {e}")
    return None

async def hit_page(session, url):
    """Makes a GET request to a page URL. We don't care about the response body."""
    try:
        # Using HEAD might be lighter if the server supports it well for this purpose
        # but GET is more universally "hitting" the page.
        async with session.get(url, headers={'User-Agent': USER_AGENT}, timeout=20) as response:
            # We don't need to read response.text() or response.content
            # Just making the request is enough.
            # Optional: log status
            if response.status // 100 == 2: # 2xx codes
                 print(f"Successfully HIT: {url} (Status: {response.status})")
            else:
                 print(f"WARN: {url} -> Status: {response.status}")
            return url, response.status
    except asyncio.TimeoutError:
        print(f"Timeout hitting page: {url}")
    except aiohttp.ClientError as e:
        print(f"Error hitting page {url}: {e}")
    return url, None

async def parse_sitemap_and_get_urls(session, sitemap_url_to_parse):
    """
    Parses a sitemap (or sitemap index) and returns a set of page URLs
    and a set of further sitemap URLs to process.
    """
    page_urls = set()
    sitemap_index_urls = set()

    content = await fetch_url_content(session, sitemap_url_to_parse)
    if not content:
        return page_urls, sitemap_index_urls

    try:
        root = ET.fromstring(content)

        # Check for sitemap index files (<sitemapindex><sitemap><loc>...</loc>...)
        for sitemap_tag in root.findall('.//sm:sitemap/sm:loc', SITEMAP_NAMESPACE):
            if sitemap_tag.text:
                sitemap_index_urls.add(sitemap_tag.text.strip())

        # Check for page URLs (<urlset><url><loc>...</loc>...)
        for url_tag in root.findall('.//sm:url/sm:loc', SITEMAP_NAMESPACE):
            if url_tag.text:
                page_urls.add(url_tag.text.strip())

    except ET.ParseError as e:
        print(f"Error parsing XML for {sitemap_url_to_parse}: {e}")
    
    return page_urls, sitemap_index_urls

async def crawl_sitemaps_and_hit_pages(initial_sitemap_url, max_concurrent_hits=50):
    """
    Main coroutine to crawl sitemaps and hit all found page URLs concurrently.
    """
    all_page_urls_to_hit = set()
    sitemaps_to_process_queue = [initial_sitemap_url]
    processed_sitemaps = set()

    async with aiohttp.ClientSession() as session:
        # Phase 1: Discover all URLs from sitemaps (including sitemap indexes)
        print("--- Phase 1: Discovering URLs from Sitemaps ---")
        while sitemaps_to_process_queue:
            current_sitemap = sitemaps_to_process_queue.pop(0)
            if current_sitemap in processed_sitemaps:
                continue
            
            processed_sitemaps.add(current_sitemap)
            
            page_urls, sitemap_index_urls = await parse_sitemap_and_get_urls(session, current_sitemap)
            
            all_page_urls_to_hit.update(page_urls)
            
            for s_index_url in sitemap_index_urls:
                if s_index_url not in processed_sitemaps:
                    sitemaps_to_process_queue.append(s_index_url)
        
        if not all_page_urls_to_hit:
            print("No page URLs found in the sitemap(s).")
            return

        print(f"\n--- Phase 2: Hitting {len(all_page_urls_to_hit)} discovered pages ---")
        
        # Create tasks for hitting pages
        tasks = []
        for url in all_page_urls_to_hit:
            tasks.append(hit_page(session, url))
            if len(tasks) >= max_concurrent_hits:
                await asyncio.gather(*tasks) # Process a batch
                tasks = []
        
        if tasks: # Process any remaining tasks
            await asyncio.gather(*tasks)

        print("\n--- All pages processed. ---")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hit all pages in a sitemap (including sitemap indexes).")
    parser.add_argument("sitemap_url", help="The URL of the main sitemap.xml file.")
    parser.add_argument(
        "-c", "--concurrent", 
        type=int, 
        default=50, 
        help="Maximum number of concurrent page hits (default: 50)."
    )
    args = parser.parse_args()

    if not args.sitemap_url.startswith(('http://', 'https://')):
        print("Error: Sitemap URL must start with http:// or https://")
    else:
        try:
            asyncio.run(crawl_sitemaps_and_hit_pages(args.sitemap_url, args.concurrent))
        except KeyboardInterrupt:
            print("\nProcess interrupted by user.")
