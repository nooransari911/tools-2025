import asyncio
import multiprocessing
from playwright.async_api import async_playwright


# Async function to scrape internships from a single URL
async def scrape_internships(url, browser, internships):
    page = await browser.new_page()  # Open a new page for each URL
    
    # Go to the URL
    await page.goto(url)
    
    # Wait for the page to load completely
    await page.wait_for_load_state('load')

    # Extract all 'href' attributes from <a> tags with class 'job-title-href'
    links = await page.query_selector_all('a.job-title-href')

    for link in links:
        href = await link.get_attribute('href')  # Get the href attribute
        text = await link.inner_text()  # Get the inner text

        if href:  # Ensure the href attribute exists
            internships.append({'href': href, 'text': text})


    # Remove duplicates based on the 'href' key (this ensures unique internships by 'href')
    internships = list({internship['href']: internship for internship in internships}.values())


    await page.close()


# Function to launch the browser and process URLs concurrently
async def scrape_multiple_urls(urls):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Headless mode for efficiency

        internships = []  # Shared list to store results

        # Create a list of async tasks for each URL
        tasks = [scrape_internships(url, browser, internships) for url in urls]

        # Run the tasks concurrently
        await asyncio.gather(*tasks)

        await browser.close()

        return internships


# Function to distribute URLs across multiple processes
def parallel_scraping(urls):
    # Number of processes to run concurrently
    num_processes = min(len(urls), multiprocessing.cpu_count())

    # Split the URLs into chunks for each process
    url_batches = [urls[i::num_processes] for i in range(num_processes)]

    with multiprocessing.Pool(processes=num_processes) as pool:
        # Each process will call `run_async_scraping` with a batch of URLs
        results = pool.map(run_async_scraping, url_batches)

    # Flatten the results from all processes
    flattened_results = [item for sublist in results for item in sublist]

    # Remove duplicates based on 'href'
    unique_internships = list({internship['href']: internship for internship in flattened_results}.values())


    print ("Total unique is:", len (unique_internships))
    
    # Write results to a file
    with open('Ilist.txt', 'w') as file:
        for internship in unique_internships:
            file.write(f"{internship['text']}: https://internshala.com{internship['href']}\n")


# Wrapper function to run asyncio event loop in a process
def run_async_scraping(urls):
    # Run the asynchronous scraping process for the given batch of URLs
    return asyncio.run(scrape_multiple_urls(urls))


if __name__ == '__main__':
    # List of URLs to scrape
    urls = [
        'https://internshala.com/internships/work-from-home-internships',
        'https://internshala.com/internships/work-from-home-internships/page-2/',
        'https://internshala.com/internships/work-from-home-internships/page-3/',
        'https://internshala.com/internships/work-from-home-internships/page-4/',
        'https://internshala.com/internships/keywords-electronics/'
        # Add more URLs here as needed
    ]

    # Start parallel scraping with multiprocessing
    parallel_scraping(urls)
