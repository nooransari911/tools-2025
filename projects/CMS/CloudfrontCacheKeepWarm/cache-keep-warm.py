# lambda_function.py
import asyncio
import aiohttp
import os
import boto3

# --- Configuration ---
# Set these as Environment Variables in the Lambda console
S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
S3_KEY = os.environ['S3_KEY']  # Path to your links.txt in the S3 bucket

# Create the S3 client once, outside the handler
s3_client = boto3.client('s3')

async def warm_url(session, url):
    """Asynchronously hits a single URL with a HEAD request to warm the cache."""
    try:
        # Using HEAD is more efficient - we only need the headers to warm the cache.
        async with session.head(url, timeout=15) as response:
            # We can check the 'X-Cache' header to see if it was a Hit or Miss from CloudFront
            cache_status = response.headers.get('X-Cache', 'Unknown')
            print(f"WARMED: {response.status} | {cache_status} | {url}")
    except Exception as e:
        print(f"FAILED to warm {url}. Reason: {type(e).__name__}")


async def main():
    """Main async function to coordinate all requests."""
    print("Starting CDN cache warming process.")
    
    try:
        # Read the list of URLs from an S3 bucket for easy updates
        s3_object = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=S3_KEY)
        content = s3_object['Body'].read().decode('utf-8')
        urls = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith('#')]
    except Exception as e:
        print(f"FATAL: Could not read URL list from S3 bucket '{S3_BUCKET_NAME}' with key '{S3_KEY}'. Error: {e}")
        return

    if not urls:
        print("No URLs found in the file. Exiting.")
        return
        
    print(f"Warming {len(urls)} URLs...")
    
    # Using a TCPConnector to limit concurrent connections if needed (e.g., to not overload a small origin)
    # connector = aiohttp.TCPConnector(limit_per_host=20)
    async with aiohttp.ClientSession() as session:
        tasks = [warm_url(session, url) for url in urls]
        await asyncio.gather(*tasks)
    
    print(f"Completed cache warming for {len(urls)} URLs.")


def lambda_handler(event, context):
    """The entry point for AWS Lambda, triggered by EventBridge."""
    asyncio.run(main())
    return {
        'statusCode': 200,
        'body': 'Cache warming process finished. Check CloudWatch Logs for details.'
    }
