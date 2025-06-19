# html_table_selector/data_fetcher.py

import re
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

class DynamicDataFetcher:
    """
    Responsible for fetching dynamically rendered HTML content from a URL
    using Playwright to control a web browser.
    """

    async def fetch(self, url: str, wait_for_selector: str) -> str:
        """
        Fetches the dynamically rendered HTML content from the given URL.

        It launches a headless browser, waits for the initial content, CLICKS
        the "Show more" button if it exists, and then returns the final page's HTML.

        Args:
            url: The URL of the webpage to fetch.
            wait_for_selector: A CSS selector for the initial element to wait for.

        Returns:
            The rendered HTML content as a string.

        Raises:
            PlaywrightTimeoutError: If the initial element does not appear.
        """
        print("Initializing Playwright browser...")
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, channel="chrome")
            page = await browser.new_page()

            try:
                print(f"Navigating to {url}...")
                await page.goto(url, wait_until="domcontentloaded")

                print(f"Waiting for element with selector '{wait_for_selector}'...")
                await page.wait_for_selector(wait_for_selector, timeout=15000)
                print("Initial table found.")

                # --- NEW LOGIC: Click the "Show more" button if it exists ---
                try:
                    # Use a regular expression to find the button robustly
                    show_more_button = page.get_by_text(re.compile(r"Show \d+ more"))
                    print("Found 'Show more' button. Clicking to expand table...")
                    await show_more_button.click(timeout=5000)
                    # Wait for the network to be idle after the click to ensure data loads
                    await page.wait_for_load_state('networkidle', timeout=5000)
                    print("Table expanded.")
                except PlaywrightTimeoutError:
                    print("No 'Show more' button found or it timed out. Proceeding.")

                print("Extracting final page content.")
                content = await page.content()
                return content
            
            finally:
                await browser.close()
                print("Playwright browser closed.")
