import asyncio
from playwright.async_api import async_playwright

# Function to log the scrolling behavior and track elements
async def track_scrolling_behavior(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Launch browser in headless=False (with UI)
        page = await browser.new_page()
        # Set the viewport to a full-size screen resolution (example 1920x1080)
        await page.set_viewport_size({"width": 1920, "height": 1080})  # Full HD resolution


        # Go to the URL
        await page.goto(url)

        # Wait for the page to load completely
        await page.wait_for_load_state('load')

        # Initial setup: track scroll position and number of job listings
        prev_scroll_position = 0
        prev_count = len(await page.query_selector_all('a.job-title-href'))

        # Function to log current state
        def log_state(scroll_position, count):
            print(f"Scroll position: {scroll_position}")
            print(f"Number of job listings: {count}")
            print("-" * 40)

        # Log the initial state
        log_state(prev_scroll_position, prev_count)

        # Track scrolls manually
        while True:
            # Wait for the user to scroll manually
            await page.wait_for_timeout(1000)  # Check every 1 second for scroll

            # Get the current scroll position and number of job listings
            scroll_position = await page.evaluate('window.scrollY')  # Get the scroll position (Y axis)
            current_count = len(await page.query_selector_all('a.job-title-href'))  # Count job listings

            # Check if the scroll position or number of elements has changed
            if scroll_position != prev_scroll_position or current_count != prev_count:
                # Log the state if there is any change
                log_state(scroll_position, current_count)

                # Update previous state
                prev_scroll_position = scroll_position
                prev_count = current_count

            # Optionally, exit if the user wants to stop (could use a specific condition to break)
            # This can be set to a certain time limit or another condition as needed.

        # Close the browser when done (optional, depending on how you stop the program)
        await browser.close()

# Function to run the asynchronous tracking
async def main():
    # The URL you want to track manually scrolling behavior
    url = 'https://internshala.com/internships/work-from-home-internships'  # Modify the URL as needed
    await track_scrolling_behavior(url)

# Run the asyncio event loop to execute the script
if __name__ == "__main__":
    asyncio.run(main())
