import fitz  # The PyMuPDF library

def get_ats_raw_text_stream(pdf_path: str) -> str:
    """
    Faithfully represents how a standard ATS acquires its initial raw text stream
    from a PDF before any downstream parsing or heuristics are applied.

    The method works by:
    1. Extracting all text blocks with their spatial coordinates.
    2. Sorting these blocks top-to-bottom, then left-to-right.
    3. Concatenating the text into a single, linear stream.

    Args:
        pdf_path: The file path to the resume PDF.

    Returns:
        A string representing the raw, spatially-ordered text stream that serves
        as the input for an ATS's next processing stages.
    """
    try:
        doc = fitz.open(pdf_path)
        full_text_stream = ""

        print(f"--- Acquiring raw text stream from '{pdf_path}' ---")

        for page_num, page in enumerate(doc):
            # The "blocks" option gives us text chunks with their coordinates.
            # Format: [x0, y0, x1, y1, "text...", block_no, block_type]
            blocks = page.get_text("blocks")

            # The CORE of the simulation: sort by vertical then horizontal position.
            # block[1] is y0 (top edge), block[0] is x0 (left edge).
            blocks.sort(key=lambda block: (block[1], block[0]))

            # Reconstruct the 1D text stream from the sorted 2D blocks.
            page_text = "\n".join([b[4].strip() for b in blocks if b[4].strip()])
            
            full_text_stream += page_text
            if page_num < doc.page_count - 1:
                full_text_stream += f"\n\n--- End of Page {page_num + 1} ---\n\n"

        doc.close()
        return full_text_stream

    except FileNotFoundError:
        return f"Error: The file at {pdf_path} was not found."
    except Exception as e:
        return f"An error occurred: {e}"

# --- Example Usage ---
if __name__ == "__main__":
    # Use a resume with any layout (simple or complex) to see the result.
    # Replace 'my_resume.pdf' with your actual file path.
    resume_path = "/home/ansarimn/Downloads/Personal/Latest Resume PDF/Resume S 21 Aug 25 Libre Baskerville General Data Science.pdf" 
    
    raw_text_input = get_ats_raw_text_stream(resume_path)

    print("\n\n--- SIMULATION COMPLETE ---")
    print("The following is the raw, one-dimensional text stream that a typical")
    print("ATS would generate from your resume's layout:")
    print("==========================================================")
    print(raw_text_input)
    print("==========================================================")
    
    # Save the output to a file for detailed inspection.
    output_filename = "ats_raw_text_simulation.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(raw_text_input)
        
    print(f"\nThis raw text stream has been saved to '{output_filename}' for your review.")
