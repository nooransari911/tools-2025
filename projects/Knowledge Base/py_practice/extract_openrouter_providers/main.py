# html_table_selector/main.py

import asyncio, pprint
from data_fetcher import DynamicDataFetcher
from html_parser import HTMLParser
from element_selector import TableSelector
from table_parser import TableParser
from playwright.async_api import Error as PlaywrightError

async def main():
    """
    Main async function to orchestrate the fetching, parsing, and selection process
    from a DYNAMIC webpage using Playwright.
    """
    target_url = input ("enter target url:  ")
    
    # The CSS selector for our target table.
    # For a tag <table class="table w-full">, the selector is 'table.table.w-full'
    wait_selector = "table.table.w-full"
    
    print(f"Attempting to scrape table from dynamic page: {target_url}")

    # 1. Instantiate the components
    fetcher = DynamicDataFetcher()
    parser = HTMLParser()
    selector = TableSelector()
    table_parser = TableParser ()

    try:
        # 2. Fetch the dynamically rendered HTML (using await)
        html_content = await fetcher.fetch(target_url, wait_for_selector=wait_selector)

        # 3. Parse the HTML (This part remains synchronous)
        parsed_html = parser.parse(html_content)

        # 4. Select the specific table (This part also remains synchronous)
        target_table = selector.select_target_table(parsed_html)



        if not target_table:
            print("\nProcess failed: Target table was not found in the HTML.")
            return

        # Step 4: Parse the table tag to extract structured data
        print("\nTable selected. Parsing provider data...")
        provider_data_list = table_parser.parse_table(target_table)

        # Step 5: Process and display the final structured data
        if provider_data_list:
            print(f"\nSuccessfully extracted data for {len(provider_data_list.data)} providers.")
            print("--- Extracted Data ---")
            pprint.pprint(provider_data_list.data)
            print("----------------------")
            print("----------------------")
            provider_data_list_str = provider_data_list.model_dump_json(indent=4)
            print (provider_data_list_str)
            print("----------------------")
        else:
            print("\nCould not extract any provider data from the table.")



    except PlaywrightError as e:
        print(f"\nProcess failed: A Playwright error occurred. Error: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    # Use asyncio.run() to execute the async main function
    asyncio.run(main())
