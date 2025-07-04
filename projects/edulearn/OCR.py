import os
from typing import Any, List, Dict
import httpx
from mcp.server.fastmcp import FastMCP

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from educhain import Educhain, LLMConfig
from pydantic import BaseModel
import base64
from dotenv import load_dotenv

from mcp1 import gemini_generate_content, mcp, PYQ, PYQList, PYQQuestion, structured_gemini, structured_gemini_list, read_path

"""
@mcp.tool()
def OCR_generate_content(
    file_paths: List[str],
    file_types: List[str],
    processing_mode: str = "parallel"
) -> PYQList:
    """
    Extract text from images and PDFs using OCR via Gemini Vision and structure as PYQs.
    """
    files_content = []
    
    for file_path, file_type in zip(file_paths, file_types):
        if file_type == "pdf":
            with open(file_path, "rb") as f:
                pdf_data = f.read()
                files_content.append({
                    "type": "document",
                    "document": pdf_data,
                    "mime_type": "application/pdf"
                })
        elif file_type == "image" or file_type == "bytes":
            with open(file_path, "rb") as f:
                image_data = f.read()
                base64_image = base64.b64encode(image_data).decode('utf-8')
                files_content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                })
        else:
            content = read_path(file_path, file_type)
            files_content.append({"type": "text", "text": content})

    system_prompt = """You are a professional OCR specialist and question paper analyzer. Extract all visible text from images and PDFs, then structure them as Previous Year Question papers.
    Instructions:
    - Capture every word, number, and symbol with high accuracy. Maintain document structure. Use [unclear] for illegible text.
    - Identify the year of each question paper. Structure questions with Major_Q_Number and Sub_Q_Number.
    - Each file typically represents one question paper (PYQ). Extract question text completely.
    - Note any images, diagrams, or special formatting in image_or_other_info field.
    """
    
    if processing_mode == "serial":
        all_papers = []
        for i, file_content in enumerate(files_content):
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=[
                    {"type": "text", "text": f"Extract and structure questions from file {i+1}:"},
                    file_content
                ])
            ]
            response = gemini_generate_content(structured_gemini_list, messages)
            all_papers.append(response)
        return PYQList(papers=all_papers)
    else:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=[
                {"type": "text", "text": f"Extract and structure questions from all {len(files_content)} files. Each file should become a separate PYQ paper:"}
            ] + files_content)
        ]
        response = gemini_generate_content(structured_gemini_list, messages)
        return response
"""