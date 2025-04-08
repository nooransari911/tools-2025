# --- Add this class definition ---
from src.utils.gemini_utils import register_schema
from pydantic import BaseModel # Added for schema definition
from typing import Optional, List # Added for strong typing in schema


class PdfPageContent(BaseModel):
    """
    Represents the extracted content structure of a single PDF page,
    likely exported from a presentation slide.
    """
    page_number: int
    section: Optional[str]                       # e.g., Chapter number, broad topic
    title: Optional[str]                         # Main title text on the page/slide
    text_content: List[str]                      # List of distinct text blocks or paragraphs
    image_descriptions: List[str]                # List of descriptions for images found

@register_schema
class PdfDocument(BaseModel):
    """
    Represents the structured content extracted from multiple pages of a PDF document.
    """
    pages: List[PdfPageContent]   
