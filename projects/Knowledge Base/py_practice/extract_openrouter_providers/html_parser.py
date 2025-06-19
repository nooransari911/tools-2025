# html_table_selector/html_parser.py

from bs4 import BeautifulSoup

class HTMLParser:
    """
    Responsible for parsing an HTML string into a structured object.
    """

    def parse(self, html_content: str) -> BeautifulSoup:
        """
        Parses the given HTML content.

        Args:
            html_content: The raw HTML string.

        Returns:
            A BeautifulSoup object representing the parsed HTML.
        """
        # Using 'lxml' is generally faster than Python's built-in 'html.parser'
        return BeautifulSoup(html_content, 'lxml')
