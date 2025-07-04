import os, sys, json
from typing import Any, List, Dict
import httpx
from mcp.server.fastmcp import FastMCP

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from educhain import Educhain, LLMConfig
from pydantic import BaseModel
import base64
from dotenv import load_dotenv

# Initialize FastMCP server
mcp = FastMCP("edulearn")

# Constants
USER_AGENT = "edulearn/1.0"
load_dotenv ("/home/ansarimn/Downloads/tools-2025/projects/Knowledge Base/.env")
RESOURCE_DIR = os.path.join(os.path.dirname(__file__), "resources")

class PYQQuestion(BaseModel):
    Major_Q_Number: int
    Sub_Q_Number: str | int
    question_text: str
    image_or_other_info: str


class PYQ(BaseModel):
    Year: str
    QList: List[PYQQuestion]


class PYQList(BaseModel):
    """List of PYQ papers from OCR results"""
    papers: List[PYQ]


# Initialize Gemini model
gemini = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.environ.get("GOOGLE_API_KEY")
)

structured_gemini = gemini.with_structured_output(PYQ)
structured_gemini_list = gemini.with_structured_output(PYQList)

# Initialize Educhain client
llm_config = LLMConfig(
    custom_model=gemini
)
client = Educhain(llm_config)


def read_path(file_path: str, file_type: str):
    """Read file content as bytes or text"""
    file_content = ""
    if file_type == "bytes":
        with open(file_path, "rb") as f:
            file_content = f.read()
    elif file_type == "text":
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
    return file_content


def gemini_generate_content(gemini_model, messages: List[HumanMessage | SystemMessage]):
    """Generate content using Gemini model"""
    response = gemini_model.invoke(messages)
    return response


@mcp.tool()
def save_resource(resource_name: str, data: Any, description: str = "") -> str:
    """
    Saves any data as a named resource. Proactively use this to store important information.
    The resource_name should be a simple, descriptive filename. It is simply the resource name, no need for preceding "resources/"
    """

    # Sanitize the resource name to prevent directory traversal issues
    safe_name = os.path.basename(resource_name)
    if not safe_name.endswith(('.json', '.txt')):
        safe_name += '.json' # Default to .json if no extension

    file_path = os.path.join(RESOURCE_DIR, safe_name)

    try:
        # Ensure the resources directory exists before writing
        os.makedirs(RESOURCE_DIR, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            if isinstance(data, BaseModel):
                # If it's a Pydantic model, dump it as a nice JSON string
                f.write(data.model_dump_json(indent=4))
            elif isinstance(data, (dict, list)):
                # If it's a dict or list, dump it as JSON
                json.dump(data, f, indent=4)
            else:
                # Otherwise, just write it as a string (for analysis reports)
                f.write(str(data))
        return f"Successfully saved resource '{safe_name}'."
    except Exception as e:
        return f"Error saving resource '{safe_name}': {e}"


@mcp.tool()
def list_resources() -> List[str]:
    """Lists all currently saved resources."""
    try:
        return os.listdir(RESOURCE_DIR)
    except FileNotFoundError:
        return ["Resource directory not found."]



@mcp.tool()
def OCR_generate_content(
    file_paths: List[str],
    file_types: List[str],
    processing_mode: str = "serial"
) -> PYQList:
    """
    Extract text from images and PDFs using OCR via Gemini Vision and structure as PYQs.
    Args:
        file_paths: List of file paths to process.
        file_types: List of file types corresponding to each file path (e.g., "image", "bytes", "text").
    
    Returns:
        PYQList: A structured list of Previous Year Question papers extracted from the files.
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
            response = gemini_generate_content(structured_gemini, messages)
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


@mcp.tool()
def generate_questions_resume_role(
    source_path: str,
    source_type: str,
    num: int,
    target_role: str,
    custom_instructions: str = None
) -> Dict: # --- Type hint is now correctly Dict
    """
    Generate interview questions from resume using Educhain.
    """
    if not custom_instructions:
        custom_instructions = f"""
        You are an AI interview assistant. Job Role: {target_role}.
        Your task is to analyze the candidate's resume (Projects and Work Experience sections).
        Based on the content, generate {num} personalized interview questions relevant to the target role.
        Align questions with skills, tools, and technologies mentioned.
        Ask both conceptual and practical questions. Vary the difficulty.
        """
        
    try:
        interviewq_object = client.qna_engine.generate_questions_from_data(
            source=source_path,
            source_type=source_type,
            num=num,
            custom_instructions=custom_instructions
        )
        # --- FIX: Convert the returned object to a dictionary ---
        # This makes the function's return type consistent.
        if hasattr(interviewq_object, 'model_dump'):
            return interviewq_object.model_dump()
        elif hasattr(interviewq_object, 'dict'): # Fallback for older Pydantic
            return interviewq_object.dict()
        else: # If it's not a Pydantic model, it might be a simple object
            return vars(interviewq_object)

    except Exception as e:
        return {"error": f"Failed to generate questions: {str(e)}"}


@mcp.tool()
def generate_pyq_analysis_report(questions: PYQList) -> str: # Renamed!
    """
    Analyzes a list of PYQ papers and generates a comprehensive study report.
    Analyze Previous Year Questions (PYQs) to identify high-value questions.
    Args:
        a PYQList object with PYQ papers in papers field.
    Returns:
        A structured analysis report as a string.
    """
    system_prompt = """You are an expert educational analyst. Analyze the given PYQs.
    Focus on: Frequency, Concept Coverage, Difficulty, Question Types, and Educational Value.
    Output a structured analysis with:
    1. High-Value Questions (Top 20-30%).
    2. Category Analysis with importance weights.
    3. Difficulty Mapping.
    4. Trend Analysis.
    5. Study Recommendations.
    For each high-value question, list: text, difficulty, topic, and why it's valuable.
    """
    
    content = f"""
    Analyze the following {len(questions.papers)} Previous Year Questions:
    Questions: {questions.model_dump_json(indent=4)}
    Perform a comprehensive analysis and provide actionable insights.
    """

    print (content)
    
    messages = [SystemMessage(content=system_prompt), HumanMessage(content=content)]
    response = gemini_generate_content(gemini, messages)
    return response.content


@mcp.tool()
def generate_new_questions_given_analysis (analysis: str, num: int) -> Dict:
    """
    Generate new questions based on the provided analysis.
    Args:   
        analysis: A string containing the analysis report.
        num: Number of new questions to generate.
    Returns:
        A Dict with newly generated questions based on the analysis.
    """
    custom_instructions = """You are an expert question generator. Based on the provided analysis, generate new questions.
    Focus on:
    1. Filling gaps in knowledge.
    2. Enhancing understanding of key concepts.
    3. Varying difficulty levels.
    4. Covering diverse question types.
    Output a list of new questions with their difficulty and topic."""
    
    try:
        new_questions = client.qna_engine.generate_questions_from_data(
            source=analysis,
            source_type="text",
            num=num,
            custom_instructions=custom_instructions
        )
        # --- FIX: Convert the returned object to a dictionary ---
        # This makes the function's return type consistent.
        if hasattr(new_questions, 'model_dump'):
            return new_questions.model_dump()
        elif hasattr(new_questions, 'dict'): # Fallback for older Pydantic
            return new_questions.dict()
        else: # If it's not a Pydantic model, it might be a simple object
            return vars(new_questions)

    except Exception as e:
        return {"error": f"Failed to generate questions: {str(e)}"}




if __name__ == "__main__":
    mcp.run()
