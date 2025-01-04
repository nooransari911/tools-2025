import sys
from playwright.sync_api import sync_playwright
from threading import Event

def open_internship_links():
    # Read the selected links passed through stdin (each line will have description and URL)
    selected_lines = sys.stdin.read().strip().split('\n')
    chrome_path = "/usr/bin/google-chrome"
    playwright = sync_playwright().start()  # Start Playwright manually
    browser = playwright.chromium.launch(
        executable_path=chrome_path,  # Use the system's installed Chrome,
        headless=False
    )

    # Create a context with a viewport size (e.g., 1920x1080)
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080}  # Full HD viewport size
    )

    # Loop through each line and extract the URL
    for line in selected_lines:
        # Split the line at ": " to get the URL part
        parts = line.split(': ', 1)  # Split only at the first ": " occurrence
        if len(parts) > 1:
            url = parts[1]  # The second part is the URL
            print(f"Opening: {url}")

            # Open a new tab and navigate to the URL
            page = context.new_page()
            page.goto(url)

    print("Browser will remain open. Terminate manually to exit.")
    Event().wait()  # Wait indefinitely without closing the browser

if __name__ == "__main__":
    open_internship_links()
