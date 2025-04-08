import json
import os
import time # Optional: To make filenames more unique if needed

# --- Mock function for testing ---
# This avoids creating real files during the test run
# It also tracks calls to ensure it's being invoked when expected.
_test_file_counter = 0
_last_generated_filename = None
def save_output_file_version_json():
    """Mocks the file versioning function for testing."""
    global _test_file_counter, _last_generated_filename
    _test_file_counter += 1
    # You could make this more sophisticated (e.g., use time) if needed
    filename = f"mock_output_v{_test_file_counter}.json"
    print(f"--- MOCK save_output_file_version_json called: Would save to '{filename}' ---")
    _last_generated_filename = filename # Store for potential later checks
    return filename

# --- Test Data ---
# A list containing various scenarios to test the parsing logic
test_all_responses = [
    # 1. Valid Case (Original Example)
    'ny\n```json\n{\n  "pages": [\n    {\n      "page_number": 1,\n      "section": null,\n      "title": "Project Risk & Financial Management",\n      "text_content": [\n        "PROJECT",\n        "MANAGEGEMENT",\n        "Project Risk & Financial",\n        "Management"\n      ],\n      "image_descriptions": [\n        "A background image with hexagonal icons related to project managem."\n      ]\n    }\n  ]\n}\n```\n',
    # 2. Valid Case with extra text before/after
    'some other text before ```json\n{"data": "second object", "value": 123}\n``` and after',
    # 3. No JSON markers
    'just plain text, no json markers',
    # 4. Valid JSON, only markers
    '```json\n{"valid": true, "items": [1, 2, 3]}\n```',
    # 5. Markers present, but Invalid JSON between them
    '```json\n{"malformed": true,\n```',
    # 6. Empty String
    '',
    # 7. Non-string item in list
    None,
    # 8. Integer item in list (another non-string)
    42,
    # 9. Start marker, but no end marker
    '```json\n{"no_end_marker": true}',
    # 10. Markers present, but empty content between them (after strip)
    '```json\n   \n```',
    # 11. Valid JSON but using slightly different markers (should be skipped by default)
    '```json\n{"data": "valid but wrong end marker"}\n````', # 4 backticks at end
    # 12. Valid JSON with Windows line endings within markers
    '```json\r\n{"os": "windows", "crlf": true}\r\n```\r\n',
]

# --- Expected Results ---
# Manually determine which items should parse successfully:
# Items 1, 2, 4, 12 (assuming \r\n is handled by strip/split implicitly)
EXPECTED_SUCCESSFUL_PARSES = 4

# --- Assign Test Data ---
all_responses = test_all_responses

# --- Start Test Execution ---
print("="*20 + " TEST START " + "="*20)
print(f"Processing {len(all_responses)} items...")
print("-" * 50)

# --- Core Processing Logic (Copied from previous response) ---
parsed_objects_list = []
start_marker = "```json\n"
# IMPORTANT: Ensure end_marker matches *exactly* what you expect.
# If it could be \n``` or \r\n```, you might need more complex logic,
# but find/rfind handles basic cases well.
end_marker = "\n```"

for i, raw_response_string in enumerate(all_responses):
    print(f"\n--- Processing index {i} ---") # Add trace for which item is processed

    # Basic check if the input is a non-empty string
    if not isinstance(raw_response_string, str) or not raw_response_string.strip():
        print(f"DEBUG: Skipping index {i} because it's not a non-empty string (Type: {type(raw_response_string)}).")
        continue

    try:
        # --- Find Markers ---
        start_index = raw_response_string.find(start_marker)

        if start_index != -1:
            print(f"DEBUG: Found start marker at index {start_index}.")
            # Calculate the actual start position of the JSON content
            json_start_pos = start_index + len(start_marker)

            # Find the end marker *after* the start marker
            # Search from json_start_pos ensures we find the end marker *after* the start
            end_index = raw_response_string.find(end_marker, json_start_pos) # Use find for consistency unless overlap is a concern

            if end_index != -1:
                print(f"DEBUG: Found end marker at index {end_index}.")
                # --- Extract and Parse ---
                json_string_to_parse = raw_response_string[json_start_pos:end_index].strip()
                print(f"DEBUG: Extracted for parsing:\n---\n{json_string_to_parse[:200]}...\n---") # Show extracted data

                # Attempt to parse the extracted content
                if json_string_to_parse: # Make sure we extracted something
                    python_obj = json.loads(json_string_to_parse)
                    parsed_objects_list.append(python_obj)
                    print(f"SUCCESS: Successfully parsed JSON from index {i}")
                else:
                    print(f"WARNING: Found markers at index {i}, but content between them was empty after stripping. Skipping.")
                    continue

            else:
                # Start marker found, but no corresponding end marker afterwards
                print(f"WARNING: Found start marker '{start_marker.strip()}' but no subsequent end marker '{end_marker.strip()}' at index {i}. Skipping.")
                # print(f"DEBUG: Problematic string content (first 100 chars):\n{raw_response_string[:100]}...") # Redundant if shown above
                continue
        else:
            # Start marker not found in the string
            print(f"INFO: Start marker '{start_marker.strip()}' not found at index {i}. Assuming non-JSON format. Skipping.")
            # print(f"DEBUG: String content sample (first 100 chars):\n{raw_response_string[:100]}...")
            continue

    except json.JSONDecodeError as e:
        # Handle cases where the extracted string between markers is *still* not valid JSON
        print(f"ERROR: Failed parsing extracted JSON content at index {i}: {e}")
        # It's helpful to show the exact string that failed parsing
        print(f"DEBUG: Problematic extracted content snippet (first 100 chars):\n{json_string_to_parse[:100]}...")
        continue # Skip this invalid entry

    except Exception as e:
        # Catch any other unexpected errors during the processing of one item
        print(f"ERROR: An unexpected error occurred processing item at index {i}: {e}")
        # print(f"DEBUG: Original string content (first 100 chars):\n{raw_response_string[:100]}...")
        continue

print("\n" + "-" * 50)
print(f"Processing Complete. Successfully parsed {len(parsed_objects_list)} JSON objects.")
print("-" * 50)

# --- Step 3: Dump the list of Python objects (using mock function) ---
output_file_path = None # Initialize
if parsed_objects_list: # Only call save/dump if we have something
    output_file_path = save_output_file_version_json()
    print(f"Attempting to dump {len(parsed_objects_list)} parsed objects...")
    # In a real test, you might write to a StringIO buffer or a temp file
    # For this snippet, we just print the structure
    print("\n--- Parsed Objects List ---")
    print(json.dumps(parsed_objects_list, indent=4)) # Pretty print the result list
    print("--- End Parsed Objects List ---")

    # Example: Simulate writing (no actual file access here)
    try:
        # json.dump(...) # This would be the actual dump call if not mocking fully
        print(f"SUCCESS: (Simulated) Dumped data to '{output_file_path}'")
    except Exception as e:
         print(f"ERROR: (Simulated) Error during dumping: {e}")

else:
    print("INFO: No valid JSON objects were parsed. Mock file save and dump were skipped.")

print("\n" + "="*20 + " TEST END " + "="*20)

# --- Verification ---
print("\n--- Verification ---")
print(f"Expected successful parses: {EXPECTED_SUCCESSFUL_PARSES}")
print(f"Actual successful parses:   {len(parsed_objects_list)}")

assert len(parsed_objects_list) == EXPECTED_SUCCESSFUL_PARSES, \
    f"Test Failed: Expected {EXPECTED_SUCCESSFUL_PARSES} parsed objects, but got {len(parsed_objects_list)}"

print("Assertion Passed: Correct number of objects parsed.")

# Optional: Check if the mock save function was called the right number of times
expected_save_calls = 1 if EXPECTED_SUCCESSFUL_PARSES > 0 else 0
print(f"Expected mock save calls: {expected_save_calls}")
print(f"Actual mock save calls:   {_test_file_counter}")
assert _test_file_counter == expected_save_calls, \
    f"Test Failed: Expected {expected_save_calls} calls to save_output_file_version_json, but got {_test_file_counter}"

print("Assertion Passed: Correct number of save calls.")
print("--- Test Finished Successfully ---")


# --- Optional Cleanup (if you were creating real files) ---
# if _last_generated_filename and os.path.exists(_last_generated_filename):
#     print(f"\nCleaning up mock file: {_last_generated_filename}")
#     os.remove(_last_generated_filename)
