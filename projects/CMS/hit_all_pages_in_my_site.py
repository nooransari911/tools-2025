import asyncio
import aiohttp
import time
import uuid

# --- Configuration ---
LINKS_URL = "http://d3isj3hu8683a4.cloudfront.net/alllinks.txt"

async def warm_url(session, url, uuid_str):
    """Asynchronously hits a single URL with a GET request to warm the cache."""
    try:
        start_time = time.perf_counter()
        async with session.get(url, timeout=15) as response:
            await response.read() # Ensure body is downloaded
            end_time = time.perf_counter()
            ttfb_ms = (end_time - start_time) * 1000
            cache_status = response.headers.get('X-Cache', 'Unknown')

            # Simplify the cache status display
            if 'Miss' in cache_status:
                simplified_status = 'Miss'
            elif 'Hit' in cache_status:
                simplified_status = 'Hit '
            else:
                simplified_status = cache_status
            
            # Log with UUID
            print(f"UUID: {uuid_str} | {response.status} | {simplified_status} | {ttfb_ms:.0f}ms | {url}")
    except Exception as e:
        print(f"UUID: {uuid_str} | FAILED to warm {url}. Reason: {type(e).__name__}")

async def main():
    print("Starting CDN cache warming process (Local Mode).")
    
    # Generate UUID for this run
    invocation_uuid = str(uuid.uuid4())

    async with aiohttp.ClientSession() as session:
        # 1. Fetch the list of links
        print(f"UUID: {invocation_uuid} | Fetching URL list from source...")
        try:
            async with session.get(LINKS_URL) as response:
                if response.status != 200:
                    print(f"UUID: {invocation_uuid} | FATAL: Failed to download links. HTTP {response.status}")
                    return
                content = await response.text()
                
            urls = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith('#')]
        except Exception as e:
            print(f"UUID: {invocation_uuid} | FATAL: Could not retrieve URL list. Error: {e}")
            return

        if not urls:
            print(f"UUID: {invocation_uuid} | No URLs found in the list. Exiting.")
            return
        
        # 2. Warm the URLs
        print(f"UUID: {invocation_uuid} | Warming {len(urls)} URLs...")
        tasks = [warm_url(session, url, invocation_uuid) for url in urls]
        await asyncio.gather(*tasks)

    print(f"UUID: {invocation_uuid} | Completed cache warming for {len(urls)} URLs.")

if __name__ == "__main__":
    # Standard entry point for local execution
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProcess stopped by user.")
