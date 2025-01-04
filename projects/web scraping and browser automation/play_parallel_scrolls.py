import asyncio
import multiprocessing
from playwright.async_api import async_playwright

# Function to scrape internships from a single URL after scrolling
async def scrape_internships(url, browser, num_scrolls=4):
    page = await browser.new_page()  # Open a new page for each URL
    
    # Go to the URL
    await page.goto(url)
    
    # Wait for the page to load completely
    await page.wait_for_load_state('load')

    # Get the initial number of job listings
    initial_count = len(await page.query_selector_all('a.job-title-href'))
    print(f"Initial job listings count: {initial_count}")

    # Scroll the page 'num_scrolls' times and track the number of listings loaded
    for i in range(num_scrolls):
        print(f"Scrolling {i + 1}/{num_scrolls}...")

        # Scroll down by a larger amount to ensure lazy loading is triggered
        # Scroll the page incrementally
        await page.evaluate('window.scrollBy(0, window.innerHeight * 1.5);')

        # Wait for the content to load after the scroll
        await page.wait_for_timeout(4000)  # Allow 2 seconds to let the new content load

        # Get the updated number of job listings after scrolling
        updated_count = len(await page.query_selector_all('a.job-title-href'))
        print(f"Updated job listings count after scroll {i + 1}: {updated_count}")
        print(f"New listings loaded this scroll: {updated_count - initial_count}")
        
        # Update the initial count for the next iteration
        initial_count = updated_count

    # After scrolling, extract all 'href' attributes from <a> tags with class 'job-title-href'
    links = await page.query_selector_all('a.job-title-href')

    internships = []

    for link in links:
        href = await link.get_attribute('href')  # Get the href attribute
        text = await link.inner_text()  # Get the inner text

        if href:  # Ensure the href attribute exists
            internships.append({'href': href, 'text': text})

    # Print the results
    for internship in internships:
        print(f"{internship['href']}\n{internship['text']}\n")

    # Close the page
    await page.close()

# Function to launch the browser and process URLs concurrently
async def scrape_multiple_urls(urls):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Headless mode for efficiency

        # Create a list of async tasks for each URL
        tasks = [scrape_internships(url, browser) for url in urls]

        # Run the tasks concurrently
        await asyncio.gather(*tasks)

        # Close the browser after all tasks are completed
        await browser.close()

# Function to distribute URLs across multiple processes
def parallel_scraping(urls):
    # Number of processes to run concurrently
    num_processes = min(len(urls), multiprocessing.cpu_count())

    # Split the URLs into chunks for each process
    url_batches = [urls[i::num_processes] for i in range(num_processes)]

    # Create a pool of processes
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Each process will call `run_async_scraping` with a batch of URLs
        pool.map(run_async_scraping, url_batches)

# Wrapper function to run asyncio event loop in a process
def run_async_scraping(urls):
    # Run the asynchronous scraping process for the given batch of URLs
    asyncio.run(scrape_multiple_urls(urls))

if __name__ == '__main__':
    # List of URLs to scrape
    urls = [
        'https://internshala.com/internships/work-from-home-internships'
        # Add more URLs here as needed
    ]
    
    # Start parallel scraping with multiprocessing
    parallel_scraping(urls)
