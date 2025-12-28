import asyncio
import aiohttp
import time
import uuid

# --- Configuration ---
LINKS_URL = "http://d3isj3hu8683a4.cloudfront.net/alllinks.txt"
CONCURRENCY_LIMIT = 20  # 20 is safe for 128MB Lambda with Keep-Alive
REQUEST_TIMEOUT = 30    

async def warm_url(session, url, uuid_str):
    try:
        start_time = time.perf_counter()
        
        # 1. We just get the headers first
        async with session.get(url) as response:
            # 2. STOP THE TIMER HERE for TTFB
            ttfb_end = time.perf_counter()
            
            # 3. Now download the body (to ensure CF caches it)
            await response.read() 
            
            total_end = time.perf_counter()

            ttfb_ms = (ttfb_end - start_time) * 1000
            total_ms = (total_end - start_time) * 1000
            
            cache_status = response.headers.get('X-Cache', 'Unknown')
            
            # Formatting for readable logs
            if 'Miss' in cache_status:
                simplified_status = 'Miss'
            elif 'Hit' in cache_status:
                simplified_status = 'Hit '
            else:
                simplified_status = cache_status
            
            # Log TTFB (Latency) separate from Total Time (Bandwidth)
            print(f"UUID: {uuid_str} | {response.status} | {simplified_status} | TTFB: {ttfb_ms:.0f}ms | Total: {total_ms:.0f}ms | {url}")

    except Exception as e:
        print(f"UUID: {uuid_str} | FAILED {url} | {type(e).__name__}")

async def main():
    print("Starting CDN cache warming (Keep-Alive Mode).")
    invocation_uuid = str(uuid.uuid4())

    # force_close=False (Default): Reuses SSL connections. FASTER.
    # limit=CONCURRENCY_LIMIT: Limits active connections.
    connector = aiohttp.TCPConnector(limit=CONCURRENCY_LIMIT)
    timeout_settings = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout_settings) as session:
        # Fetch list
        try:
            async with session.get(LINKS_URL) as response:
                if response.status != 200:
                    print(f"FAILED to download links. HTTP {response.status}")
                    return
                content = await response.text()     
            urls = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith('#')]
        except Exception as e:
            print(f"FATAL: Could not retrieve URL list. {e}")
            return

        if not urls:
            print("No URLs found.")
            return
        
        print(f"UUID: {invocation_uuid} | Warming {len(urls)} URLs...")
        
        # Fire requests
        tasks = [warm_url(session, url, invocation_uuid) for url in urls]
        await asyncio.gather(*tasks)

    print(f"UUID: {invocation_uuid} | Completed.")

if __name__ == "__main__":
    asyncio.run(main())
