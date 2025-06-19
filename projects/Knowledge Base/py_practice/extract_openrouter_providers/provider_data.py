# html_table_selector/provider_data.py
from pydantic import BaseModel
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ProviderData ():
    """
    A structured data object representing a single provider's details.
    Each field is optional to handle cases where data might be missing on the page.
    """
    name: Optional[str]
    context: Optional[str]
    max_output: Optional[str]
    cost_input: Optional[str]
    cost_output: Optional[str]
    throughput: Optional[str]



class ProviderDataList (BaseModel):
    data: Optional [List [ProviderData]]
