**Analyze and Evaluate JSON Files for PDF Content Accuracy**

**Context:** You are provided with multiple JSON files (`output response v13.json`, `output response v14.json`, `output response v15.json`, `output response v16.json`), each representing structured data extracted from the same set of PDF presentations.

**Task:** Compare these JSON files to determine which one offers the most accurate and complete representation of the original PDF content.

**Primary Goal:** Maximize information preservation and accuracy. The internal formatting or readability of the JSON structure itself is a secondary concern compared to capturing all original content correctly.

**Evaluation Criteria (in order of importance):**

1.  **Completeness of Text Extraction:**
    *   Does the `text_content` capture all text from the main body of the slides?
    *   Crucially, is text visible *within images* (e.g., labels on diagrams, text in screenshots) successfully extracted and included in the JSON data (`text_content` or potentially `image_descriptions`)? Check for omissions compared across versions.
2.  **Accuracy of Text Extraction:**
    *   Is the extracted `text_content` free from significant OCR errors?
    *   Are special characters preserved correctly?
3.  **Accuracy of Structural Information:**
    *   How accurate and semantically meaningful are the assigned `section` titles? More specific and correct sectioning is preferred.
    *   Are `page_number` and `title` fields correct?
4.  **Quality of Image Descriptions:**
    *   Are `image_descriptions` relevant and sufficiently detailed to provide context about the visual elements on the slides?

**Output:**

1.  Identify the filename of the JSON file deemed the best based on the above criteria, prioritizing information completeness and accuracy.
2.  Provide a concise justification explaining *why* the selected file is superior, specifically referencing which criteria it met better than the others (e.g., "captured text from image on page X," "had more accurate section titles," "corrected omissions found in other versions").
