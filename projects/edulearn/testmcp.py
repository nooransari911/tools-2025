import asyncio
import os
import sys
import json
from mcp1 import (
    OCR_generate_content,
    generate_questions_resume_role,
    analyze_PYQ,
    PYQList,
    PYQ,
    PYQQuestion
)

# --- Test functions are now refactored to return data for the report ---

def run_ocr_tool():
    """Wrapper to run the synchronous OCR tool."""
    test_files = [
        "/home/ansarimn/Pictures/Screenshots/Screenshot_20250703_172559.png",
        "/home/ansarimn/Pictures/Screenshots/Screenshot_20250703_172615.png",
        "/home/ansarimn/Pictures/Screenshots/Screenshot_20250703_172642.png"
    ]
    file_types = ["image", "image", "image"]
    
    existing_files = [p for p in test_files if os.path.exists(p)]
    existing_types = [t for p, t in zip(test_files, file_types) if os.path.exists(p)]
    
    if not existing_files:
        return None, "No test files found. Mock data will not be used."
    
    try:
        result = OCR_generate_content(existing_files, existing_types, "parallel")
        return result, f"Successfully processed {len(result.papers)} paper(s) from {len(existing_files)} file(s)."
    except Exception as e:
        return None, f"OCR test failed: {e}"

def run_resume_questions_tool():
    """Wrapper for the resume question generation tool."""
    resume_path = "/home/ansarimn/Downloads/Resume S 01 July 2025 AI.pdf"
    if not os.path.exists(resume_path):
        return None, "Resume file not found. Skipping test."
    
    try:
        role = "Python Developer"
        result = generate_questions_resume_role(
            source_path=resume_path,
            source_type="pdf",
            num=5,
            target_role=role
        )
        return result, f"Successfully generated questions for role: {role}."
    except Exception as e:
        return None, f"Resume questions test failed: {e}"

def run_analyze_pyq_tool(pyq_data: PYQList):
    """Wrapper for the PYQ analysis tool."""
    if not pyq_data or not pyq_data.papers:
        return None, "No PYQ data available for analysis."
    
    try:
        # Analyze the first paper for the report
        paper_to_analyze = pyq_data.papers[0]
        analysis_result = analyze_PYQ(paper_to_analyze)
        return analysis_result, f"Successfully analyzed paper from year {paper_to_analyze.Year}."
    except Exception as e:
        return None, f"PYQ analysis test failed: {e}"

async def main():
    """Main async test runner that orchestrates tests and generates a report."""
    report_content = ["# Test Suite Results\n\n"]
    
    # --- 1. OCR Tool Test ---
    print("🧪 Running OCR Tool Test...")
    report_content.append("## 1. OCR Tool Results\n\n")
    
    # Run the synchronous function in an executor to avoid blocking
    loop = asyncio.get_running_loop()
    pyq_data, ocr_summary = await loop.run_in_executor(None, run_ocr_tool)
    
    print(f"   -> {ocr_summary}")
    report_content.append(f"**Summary:** {ocr_summary}\n\n")
    if pyq_data:
        report_content.append("### Full OCR Output (JSON)\n\n")
        report_content.append("```json\n")
        report_content.append(pyq_data.model_dump_json(indent=2))
        report_content.append("\n```\n\n")
    
    # --- 2. Resume Questions Tool Test ---
    print("\n🧪 Running Resume Questions Tool Test...")
    report_content.append("## 2. Resume Questions Tool Results\n\n")
    
    resume_result, resume_summary = await loop.run_in_executor(None, run_resume_questions_tool)
    
    print(f"   -> {resume_summary}")
    report_content.append(f"**Summary:** {resume_summary}\n\n")
    if resume_result:
        report_content.append("### Generated Questions (JSON)\n\n")
        report_content.append("```json\n")
        report_content.append(json.dumps(resume_result, indent=2))
        report_content.append("\n```\n\n")

    # --- 3. PYQ Analysis Tool Test ---
    print("\n🧪 Running PYQ Analysis Tool Test...")
    report_content.append("## 3. PYQ Analysis Results\n\n")

    analysis_result, analysis_summary = await loop.run_in_executor(None, run_analyze_pyq_tool, pyq_data)

    print(f"   -> {analysis_summary}")
    report_content.append(f"**Summary:** {analysis_summary}\n\n")
    if analysis_result:
        report_content.append("### Full Analysis Text\n\n")
        report_content.append(analysis_result)
        report_content.append("\n\n")

    # --- Write final report to file ---
    report_filename = "results.md"
    with open(report_filename, "w", encoding="utf-8") as f:
        f.write("".join(report_content))
    
    print(f"\n✅ All tests completed! Report saved to '{report_filename}'.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nTest suite interrupted by user.")
        sys.exit(0)
