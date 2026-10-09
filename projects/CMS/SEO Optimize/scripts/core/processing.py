# processing.py
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

import file_operations
import ai_operations

logger = logging.getLogger(__name__)

def process_single_file(file_path: str) -> None:
    """
    Executes the full read -> get queries -> optimize -> backup -> write sequence for one file.
    """
    logger.info(f"--- Starting processing for: {file_path} ---")
    try:
        # 1. Read original content
        original_content = file_operations.read_file_content(file_path)
        if original_content is None:
            # Error is already logged in the read function
            return

        # 2. Call AI to get relevant queries
        queries = ai_operations.get_relevant_queries(original_content)
        if not queries:
            logger.error(f"Could not generate queries for '{file_path}'. Skipping.")
            return

        # 3. Call AI to optimize content for the queries
        optimized_content = ai_operations.optimize_content_for_queries(original_content, queries)
        if not optimized_content:
            logger.error(f"Could not generate optimized content for '{file_path}'. Skipping.")
            return

        # 4. Backup original file
        if not file_operations.backup_original_file(file_path):
            logger.error(f"Failed to backup '{file_path}'. New content will not be written.")
            return

        # 5. Write new content
        file_operations.write_new_content(file_path, optimized_content)
        
        logger.info(f"--- Successfully completed processing for: {file_path} ---")

    except Exception as e:
        logger.critical(f"An unhandled exception occurred while processing '{file_path}': {e}", exc_info=True)


def process_batch(file_path_batch: list[str]) -> None:
    """
    Processes a batch of file paths in parallel using a thread pool.
    """
    logger.info(f"Processing batch of {len(file_path_batch)} files in parallel...")
    with ThreadPoolExecutor(max_workers=len(file_path_batch)) as executor:
        # Submit all tasks to the pool
        future_to_path = {executor.submit(process_single_file, path): path for path in file_path_batch}
        
        # Wait for tasks to complete and log results/errors
        for future in as_completed(future_to_path):
            path = future_to_path[future]
            try:
                # The function itself doesn't return anything, but this will raise exceptions
                future.result()
            except Exception as exc:
                logger.error(f"'{path}' generated an exception in the thread pool: {exc}")
    logger.info("Batch processing complete.")
