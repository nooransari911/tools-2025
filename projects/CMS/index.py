import os
import sys
import time
import requests
import xml.etree.ElementTree as ET
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# --- Configuration ---
# The full URL of your sitemap or sitemap index file
SITEMAP_URL = "https://d3isj3hu8683a4.cloudfront.net/limited-sitemap.xml" 

# The path to your Google Cloud service account JSON credentials file
GOOGLE_CREDENTIALS_FILE = '/home/ansarimn/Downloads/archive/sensitive/optimum-task-411411-228b76a59dc6-search-engine.json'

# The scope required for the Google Indexing API
SCOPES = ['https://www.googleapis.com/auth/indexing']

# The endpoint for the Google Indexing API
INDEXING_API_ENDPOINT = 'https://indexing.googleapis.com/v3/urlNotifications:publish'
# --- End of Configuration ---

def fetch_and_parse_sitemap(url):
    """
    Fetches a sitemap or sitemap index and recursively parses it to get all URLs.
    """
    print(f"Fetching sitemap: {url}")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status() # Raise an exception for bad status codes
    except requests.RequestException as e:
        print(f"Error fetching sitemap {url}: {e}")
        return []

    xml_content = response.content
    root = ET.fromstring(xml_content)
    namespace = root.tag.split('}')[0] + '}' # Extract namespace

    urls = []
    # Check if it is a sitemap index file
    if root.tag.endswith('sitemapindex'):
        for sitemap in root.findall(f'{namespace}sitemap'):
            loc = sitemap.find(f'{namespace}loc')
            if loc is not None:
                # Recursive call to handle nested sitemaps
                urls.extend(fetch_and_parse_sitemap(loc.text))
    # Check if it is a standard URL set
    elif root.tag.endswith('urlset'):
        for url_element in root.findall(f'{namespace}url'):
            loc = url_element.find(f'{namespace}loc')
            if loc is not None:
                urls.append(loc.text)
    
    return list(set(urls)) # Use set to remove duplicates, then convert to list

def submit_url_to_google(url, credentials):
    """
    Submits a single URL to the Google Indexing API.
    """
    payload = {
        'url': url,
        'type': 'URL_UPDATED'
    }
    
    try:
        authed_session = Request()
        credentials.refresh(authed_session) # Refresh credentials
        
        response = requests.post(
            INDEXING_API_ENDPOINT,
            json=payload,
            headers={'Authorization': f'Bearer {credentials.token}'},
            timeout=10
        )
        
        # Check the response
        if response.status_code == 200:
            print(f"✅ Successfully submitted: {url}")
            return True
        else:
            print(f"❌ Failed to submit: {url}")
            print(f"   Status Code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ An exception occurred while submitting {url}: {e}")
        return False

def main():
    """
    Main function to orchestrate the process.
    """
    print("--- Starting Google Indexing Script ---")

    # 1. Check for credentials file
    if not os.path.exists(GOOGLE_CREDENTIALS_FILE):
        print(f"ERROR: Credentials file not found at '{GOOGLE_CREDENTIALS_FILE}'")
        print("Please follow the prerequisite steps to create and download it.")
        sys.exit(1)

    # 2. Authenticate with Google
    try:
        credentials = service_account.Credentials.from_service_account_file(
            GOOGLE_CREDENTIALS_FILE, scopes=SCOPES
        )
        # print (credentials)
    except Exception as e:
        print(f"Error loading credentials: {e}")
        sys.exit(1)

    # 3. Fetch and parse all URLs from the sitemap
    all_urls = fetch_and_parse_sitemap(SITEMAP_URL)

    if not all_urls:
        print("No URLs found in the sitemap. Exiting.")
        sys.exit(0)
    
    print(f"\nFound a total of {len(all_urls)} unique URLs to submit.\n")

    # 4. Submit each URL to the API
    success_count = 0
    fail_count = 0
    for i, url in enumerate(all_urls):
        print(f"Submitting URL {i+1}/{len(all_urls)}...")
        if submit_url_to_google(url, credentials):
            success_count += 1
        else:
            fail_count += 1
        
        # Be a good citizen and don't spam the API. A short delay can help.
        time.sleep(0.2) 

    print("\n--- Submission Complete ---")
    print(f"Successfully submitted: {success_count}")
    print(f"Failed to submit: {fail_count}")
    print("---------------------------")


if __name__ == "__main__":
    main()
