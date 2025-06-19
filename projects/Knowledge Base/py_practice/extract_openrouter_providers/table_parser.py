# html_table_selector/table_parser.py

from typing import Dict, List, Optional
from bs4.element import Tag
from provider_data import ProviderData, ProviderDataList

class TableParser:
    """
    Responsible for parsing a complex HTML table structure and
    extracting structured data from it. It intelligently finds data
    by mapping text labels to their values.
    """

    def _get_text_from_tag(self, tag: Tag, selector: str) -> Optional[str]:
        """Safely finds a sub-tag and returns its stripped text."""
        found_tag = tag.find(selector)
        return found_tag.get_text(strip=True) if found_tag else None

    def _parse_row(self, row_tag: Tag) -> Optional[ProviderData]:
        """
        Parses a single complex table row (tr) into a ProviderData object.
        This function is designed to be robust against the nested div/span structure.
        """
        cells = row_tag.find_all('td', recursive=False)
        if len(cells) < 2:
            return None

        try:
            # --- Extract Provider Name from the first cell ---
            provider_name = self._get_text_from_tag(cells[0], 'a')
            if not provider_name:
                return None # Skip if there's no provider name link

            # --- Extract All Metrics from the second cell into a dictionary ---
            metrics_cell = cells[1]
            metrics_map: Dict[str, str] = {}
            
            # Find all divs that act as containers for a label-value pair.
            metric_divs = metrics_cell.find_all('div', class_="flex-col")

            for div in metric_divs:
                # The label is in a div with class 'text-xs'
                label_tag = div.find('div', class_='text-xs')
                # The value is in a span with class 'text-lg'
                value_tag = div.find('span', class_='text-lg')

                if label_tag and value_tag:
                    label = label_tag.get_text(strip=True)
                    # Get all text within the value tag, handling nested units
                    value_text = value_tag.get_text(strip=True, separator=' ').split(' ')[0]
                    metrics_map[label] = value_text

            # --- Create the structured object from the metrics map ---
            # Using .get() provides safety if a metric is missing for a provider.
            return ProviderData(
                name=provider_name,
                context=metrics_map.get('Context'),
                max_output=metrics_map.get('Max Output'),
                cost_input=metrics_map.get('Input'),
                cost_output=metrics_map.get('Output'),
                throughput=metrics_map.get('Throughput')
            )

        except (AttributeError, IndexError) as e:
            print(f"Warning: Could not parse a row. Skipping. Error: {e}")
            return None

    def parse_table(self, table_tag: Tag) -> ProviderDataList:
        """
        Takes a BeautifulSoup Tag representing the table and returns a list
        of structured ProviderData objects.
        """
        provider_list = ProviderDataList (data=[])

        tbody = table_tag.find('tbody')
        if not tbody:
            return []

        rows = tbody.find_all('tr', recursive=False)
        print(f"Found {len(rows)} total provider rows to parse.")

        for row in rows:
            provider_data = self._parse_row(row)
            if provider_data:
                provider_list.data.append(provider_data)


        return provider_list
