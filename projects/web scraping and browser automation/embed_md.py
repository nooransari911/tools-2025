import requests, subprocess
from bs4 import BeautifulSoup
import urllib.parse

def fetch_display_text(url):
    try:
        # Make an HTTP request to fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes (4xx or 5xx)

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to find the <title> tag as the display text
        title = soup.find('title')
        
        # If the <title> tag is found, return its content; otherwise, return a fallback
        if title:
            return title.get_text().strip()
        else:
            return "No title found"
    
    except requests.exceptions.RequestException as e:
        # In case of an error (e.g., network error, invalid URL, etc.)
        return f"Error fetching the URL: {e}"

def embed_links_in_markdown():
    links = []
    
    while True:
        # Get the URL from the user
        url = input("Enter the URL (or type 'qq' to finish): ").strip()
        if url.lower() == 'qq':
            break
        
        # Ensure the URL starts with 'http://' or 'https://' for proper parsing
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url  # Prepend 'http://' if missing
        
        # Fetch display text dynamically from the URL
        display_text = fetch_display_text(url)
        
        # Add the URL and display text as a tuple to the links list
        links.append((url, display_text))


    print ("\n\n")


    markdown_links = ""
    # Generate the markdown formatted string
    for url, text in links:
        markdown_links += f"- [{text}]({url})\n"
    
    # Print the markdown links
    print(markdown_links)

    # Copy the markdown links to clipboard using wl-copy
    subprocess.run(['wl-copy'], input=markdown_links.encode(), check=True)

# Example usage
embed_links_in_markdown()
