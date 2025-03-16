"""from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Make sure it's Chromium
    page = browser.new_page()
    page.goto('https://www.amazon.com')
    page.screenshot(path='amz.png')
    time.sleep (10)
    browser.close()



"""



from playwright.sync_api import sync_playwright

# Run the script
with sync_playwright() as p:
    # Launch the browser (Chromium)
    browser = p.chromium.launch(headless=False)  # Set headless=True to run without UI
    page = browser.new_page()

    # Go to the URL containing the page
    page.goto('https://internshala.com/internships/work-from-home-internships')  # Replace with the actual URL

    # Wait for the page to load completely
    page.wait_for_load_state('load')  # Ensures that the page is fully loaded

    # Extract all 'href' attributes from <a> tags with class 'job-title-href'
    links = page.locator('a.job-title-href')

    # Generate a list of href values
    internship = {}
    # href_links = []
    # inner_text = []

    for link in links.all():
        href = link.get_attribute('href')  # Get the href attribute
        text = link.inner_text ()  # Get the inner text (not inner_text())()

        if href:  # Ensure the href attribute exists
            internship['href'] = href  # Store href value
            internship['text'] = text  # Store text value

            print(f"{internship['href']}\n{internship['text']}\n")    

    # Close the browser
    browser.close()


