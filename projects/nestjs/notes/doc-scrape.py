from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from html import unescape

def get_website_content_and_convert_to_markdown(url):
    """
    Fetches content from a URL using Playwright, waits for dynamic content,
    extracts specific inner HTML (using XPath), and converts it to Markdown.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Launch Chromium in headless mode
        page = browser.new_page()

        try:
            page.goto(url, timeout=120000)

            # Wait for the specific element to be present (adjust timeout as needed)
            xpath_expression = "//div[@class='content']"
            target_element = page.wait_for_selector(f"xpath={xpath_expression}", timeout=20000)

            # Get the inner HTML of the target element
            inner_html = target_element.inner_html()

            return extract_text_to_markdown(inner_html)

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

        finally:
            browser.close()

def extract_text_to_markdown(html_content):
    """
    Extracts text content from HTML and converts it to Markdown dynamically
    using a recursive strategy and a tag formatting lookup table.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Tag formatting rules (add more as needed)
    tag_formatting = {
        'p': ('', '\n\n'),
        'h1': ('# ', '\n\n'),
        'h2': ('## ', '\n\n'),
        'h3': ('### ', '\n\n'),
        'h4': ('#### ', '\n\n'),
        'h5': ('##### ', '\n\n'),
        'h6': ('###### ', '\n\n'),
        'blockquote': ('> ', '\n\n'),
        'em': ('*', '*'),
        'strong': ('**', '**'),
        'a': ('[', ']'),
        'code': ('`', '`'),
        'img': ('![', ']'),
        # Lists are handled separately
    }

    def process_element(element, list_type=None, list_index=None):
        """
        Recursively processes an element and its descendants,
        building the Markdown string.
        """
        markdown = ""

        if element.name is None:  # Text node
            text = unescape(element.string)  # Preserve spaces in text nodes
            if text.strip():  # Add non-empty text with appropriate spacing
                if list_type == 'ul':
                    return f"- {text}\n"
                elif list_type == 'ol':
                    return f"{list_index}. {text}\n"
                else:
                    return text
            else:
                return ""

        prefix, suffix = tag_formatting.get(element.name, ('', ''))
        markdown += prefix

        if element.name == 'a' and element.get('href'):
            markdown += process_element(element.contents[0]) if element.contents else ''
            markdown += f"({element.get('href')})"
        elif element.name == 'img' and element.get('src'):
            alt_text = element.get('alt', '')
            markdown += alt_text
            markdown += f"({element.get('src')})"
        elif element.name == 'pre':
            code_lang = element.get("class", [""])[0].replace("language-", "")
            code_content = element.code.get_text()
            return f"```{code_lang}\n{code_content}```\n\n"
        elif element.name == 'ul':
            for i, li in enumerate(element.find_all('li', recursive=False)):
                markdown += process_element(li, list_type='ul')
            return markdown + "\n"
        elif element.name == 'ol':
            for i, li in enumerate(element.find_all('li', recursive=False)):
                markdown += process_element(li, list_type='ol', list_index=i + 1)
            return markdown + "\n"
        else:
            for child in element.contents:
                markdown += process_element(child)

        markdown += suffix
        return markdown

    return process_element(soup).strip()



# Example usage:
# url = "https://docs.nestjs.com/providers"
url = input("Enter the URL of the website to scrape: ")
markdown_output = get_website_content_and_convert_to_markdown(url)

if markdown_output:
    print(markdown_output)
