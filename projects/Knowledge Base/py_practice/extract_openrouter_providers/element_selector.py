# html_table_selector/element_selector.py

from typing import Optional
from bs4 import BeautifulSoup
from bs4.element import Tag

class TableSelector:
    """
    Responsible for selecting a specific table element from parsed HTML.
    """

    def select_target_table(self, parsed_html: BeautifulSoup) -> Optional[Tag]:
        """
        Selects the table with the specific class "table w-full".

        This class name is an example; it should be updated if the target
        website's structure changes.

        Args:
            parsed_html: A BeautifulSoup object containing the parsed page.

        Returns:
            The selected table as a bs4.element.Tag object, or None if not found.
        """
        # The selector 'table' with class 'table w-full'.
        # Note: 'class_' is used because 'class' is a reserved keyword in Python.
        selector_criteria = {'class': 'table w-full'}
        
        table = parsed_html.find('table', attrs=selector_criteria)
        return table
