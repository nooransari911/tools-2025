import os
import sys
import argparse
import requests # For HTTP requests
from typing import List, Optional
from urllib.parse import urlparse # Needed for robust path handling

# --- Constants ---
DEFAULT_TIMEOUT = 10  # seconds for HTTP requests
DEFAULT_EXTENSIONS = ["png", "jpeg", "jpg", "webp"] # Common image extensions
MAX_CONSECUTIVE_404_LIMIT = 4

# --- Single Responsibility Classes ---

class UrlGenerator:
    """
    Responsible for generating specific image URLs based on a template, index, and extension.
    The base_url_template is the part of the URL before the number.
    e.g., "https://example.com/images/pic-" or "https://example.com/images/"
    """
    def __init__(self, base_url_template: str):
        if not base_url_template:
            raise ValueError("Base URL template cannot be empty.")
        self.base_url_template = base_url_template

    def generate(self, index: int, extension: str) -> str:
        """Generates a full URL string."""
        if index < 0:
            raise ValueError("Index must be non-negative.")
        if not extension:
            raise ValueError("Extension cannot be empty.")
        clean_extension = extension.lstrip('.')
        return f"{self.base_url_template}{index}.{clean_extension}"

class HttpClient:
    """
    Responsible for making HTTP GET requests.
    """
    def __init__(self, timeout: int = DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, url: str) -> Optional[requests.Response]:
        """
        Fetches content from the given URL.
        Returns the response object on success (200 or 404), None on other errors.
        """
        try:
            response = self.session.get(url, timeout=self.timeout, stream=True)
            if response.status_code in [200, 404]:
                return response
            else:
                print(f"Error: Received status {response.status_code} for {url}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error: Network request failed for {url}: {e}")
            return None
        return None

class FileSaver:
    """
    Responsible for saving data to the file system.
    """
    def __init__(self, base_download_dir: str):
        if not base_download_dir:
            raise ValueError("Base download directory cannot be empty.")
        self.base_download_dir = base_download_dir
        self._ensure_base_dir_exists()

    def _ensure_base_dir_exists(self):
        """Ensures the base download directory exists."""
        try:
            os.makedirs(self.base_download_dir, exist_ok=True)
            print(f"Ensured base directory exists: {self.base_download_dir}")
        except OSError as e:
            print(f"Error: Could not create base directory {self.base_download_dir}: {e}")
            raise

    def save(self, content_iterator, filename: str) -> bool:
        """
        Saves the content (iterator) to a file relative to base_download_dir.
        Returns True on success, False on failure.
        """
        filepath = os.path.join(self.base_download_dir, filename)
        try:
            with open(filepath, 'wb') as f:
                for chunk in content_iterator:
                    if chunk:
                        f.write(chunk)
            print(f"Successfully saved: {filepath}")
            return True
        except IOError as e:
            print(f"Error: Could not save file {filepath}: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred while saving {filepath}: {e}")
            return False

class ImageDownloader:
    """
    Orchestrates the image downloading process.
    Determines filename based on the base URL template structure.
    """
    def __init__(self,
                 url_generator: UrlGenerator,
                 http_client: HttpClient,
                 file_saver: FileSaver,
                 extensions_to_try: List[str],
                 max_consecutive_404s: int = MAX_CONSECUTIVE_404_LIMIT):
        self.url_generator = url_generator
        self.http_client = http_client
        self.file_saver = file_saver
        # Ensure extensions are clean (e.g., "png", not ".png") for consistency
        self.extensions_to_try = [ext.lstrip('.') for ext in extensions_to_try]
        self.max_consecutive_404s = max_consecutive_404s
        # Derive the filename prefix from the UrlGenerator's base template ONCE.
        self.filename_prefix = self._derive_filename_prefix(self.url_generator.base_url_template)
        print(f"Derived filename prefix: '{self.filename_prefix}'")


    def _derive_filename_prefix(self, base_template_url: str) -> str:
        """
        Derives the filename prefix from the base URL template.
        This prefix is the part of the template that forms the beginning of the filename,
        before the number and extension are appended.

        Example:
        - "https://example.com/path/img-" -> "img-"
        - "https://example.com/path/"     -> "" (empty string)
        - "https://example.com/img-"      -> "img-" (if domain is part of template name)
        """
        parsed_url = urlparse(base_template_url)
        # os.path.basename works well here:
        # os.path.basename("/foo/bar/baz-") -> "baz-"
        # os.path.basename("/foo/bar/")    -> "" (on POSIX systems, if path ends with /)
        # os.path.basename("foo-")         -> "foo-" (if no slashes in path part)
        path_component = parsed_url.path
        
        # Ensure consistent behavior for paths like "/" or ""
        if not path_component or path_component == "/":
             # If template is "https://domain.com" or "https://domain.com/"
            return ""
            
        # If the template itself ends with a slash (e.g. "https://foo/bar/"),
        # then the "filename part" of the template is empty.
        # Otherwise, it's the last component of the path.
        if base_template_url.endswith('/'):
            return ""
        else:
            return os.path.basename(path_component)


    def download_images(self, start_index: int = 0):
        """
        Starts the download process from the given start_index.
        """
        current_index = start_index
        consecutive_404_indices = 0

        while consecutive_404_indices < self.max_consecutive_404s:
            found_image_for_current_index = False
            print(f"\n--- Processing index: {current_index} ---")

            for ext in self.extensions_to_try: # ext is now 'png', 'jpg', etc.
                url = self.url_generator.generate(current_index, ext)
                print(f"Attempting: {url}")

                response = self.http_client.get(url)

                if response and response.status_code == 200:
                    # Construct filename: <derived_prefix><number>.<extension>
                    # This matches os.path.basename(urlparse(url).path) for the given URL structure.
                    target_filename = f"{self.filename_prefix}{current_index}.{ext}"
                    
                    if self.file_saver.save(response.iter_content(chunk_size=8192), target_filename):
                        found_image_for_current_index = True
                        consecutive_404_indices = 0
                        break
                    else:
                        print(f"Failed to save {url} (as {target_filename}). Trying next extension if available.")
                
                elif response and response.status_code == 404:
                    print(f"404 Not Found: {url}")
                
                elif response is None:
                    print(f"Skipping {url} due to client error. Trying next extension if available.")
            
            if not found_image_for_current_index:
                print(f"No image found for index {current_index} with any tried extensions.")
                consecutive_404_indices += 1
                print(f"Consecutive indices with no images found: {consecutive_404_indices}/{self.max_consecutive_404s}")
            
            current_index += 1

        print(f"\nDownload process finished. Reached {consecutive_404_indices} consecutive indices with no images.")

# --- Main Program / Entry Point ---

def main():
    parser = argparse.ArgumentParser(description="Download images sequentially from a URL pattern.")
    parser.add_argument("base_dir",
                        help="Base directory to write downloaded files to.")
    parser.add_argument("base_url_template",
                        help="Base URL template (e.g., 'https://domain.com/some/path/fileprefix-'). "
                             "The number and extension will be appended. If it ends with '/', "
                             "the filename prefix is considered empty.")
    parser.add_argument("--start-index", type=int, default=0,
                        help="Starting number for image URLs (default: 0).")
    parser.add_argument("--extensions", nargs="+", default=DEFAULT_EXTENSIONS,
                        help=f"List of extensions to try (default: {' '.join(DEFAULT_EXTENSIONS)}). "
                             "Do not include leading dots.")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                        help=f"HTTP request timeout in seconds (default: {DEFAULT_TIMEOUT}).")
    parser.add_argument("--max-404s", type=int, default=MAX_CONSECUTIVE_404_LIMIT,
                        help="Number of consecutive 404s on an index to trigger stop "
                             f"(default: {MAX_CONSECUTIVE_404_LIMIT}).")

    args = parser.parse_args()

    try:
        url_gen = UrlGenerator(args.base_url_template)
        http_cli = HttpClient(timeout=args.timeout)
        file_save = FileSaver(args.base_dir)

        downloader = ImageDownloader(
            url_generator=url_gen, # ImageDownloader will get base_url_template from here
            http_client=http_cli,
            file_saver=file_save,
            extensions_to_try=args.extensions,
            max_consecutive_404s=args.max_404s
        )

        downloader.download_images(start_index=args.start_index)

    except ValueError as ve:
        print(f"Configuration Error: {ve}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected critical error occurred: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
