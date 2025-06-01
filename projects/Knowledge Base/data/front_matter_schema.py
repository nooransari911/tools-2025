from typing import List, Optional
from pydantic import BaseModel, Field, RootModel
from src.utils.gemini_utils import register_schema




class GeneratedFrontMatter(BaseModel):
    """
    Represents the structured front matter for a content page.
    This metadata is typically used for SEO, site generation, and content organization.
    """
    title: str = Field(
        ...,
        description="The main title of the content page."
    )
    list_title: Optional[str] = Field(
        default=None,
        alias="list-title",
        validation_alias="list-title",
        serialization_alias="list-title",
        description="title specifically for display on list/home pages; optionally different from title;"
    )
    subtitle: Optional[str] = Field(
        default=None,
        description="""Clarifies the title, incites curiosity, motivates reading,
or bluntly states the core irony/paradox in the essay if any, etc."""
    )
    categories: List[str] = Field(
        default_factory=list,
        description="Categories for content; narrower in scope and more specific than tags."
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Broader themes, subjects, domains, etc., associated with the content."
    )
    set_: Optional[List[str]] = Field(
        default=None,
        alias="set",
        validation_alias="set",
        serialization_alias="set",
        description="""Like tags, but explicitly forms a set of articles;
tags are standard terminology, set is that but augmented by me;
optionally sets can be nested and have subsets for a clean organization."""
    )
    description: str = Field(
        ...,
        description="Description/summary of article for SEO/search engine."
    )
    summary: Optional[str] = Field(
        default=None,
        description="""Description/summary of article but for reader;
optionally to be displayed on list pages."""
    )






@register_schema
class GeneratedFrontMatterList(RootModel[List[GeneratedFrontMatter]]):
    """
    Represents a list of GeneratedFrontMatter objects.
    This model is useful for validating or processing a collection of front matter entries,
    especially when the root JSON object is an array of front matter items.
    """
    root: List[GeneratedFrontMatter] = Field(
        description="The list of generated front matter items."
    )

    def __iter__(self):
        """Allows iterating directly over the list of front matter items."""
        return iter(self.root)

    def __getitem__(self, item):
        """Allows accessing front matter items by index."""
        return self.root[item]

    def __len__(self):
        """Returns the number of front matter items in the list."""
        return len(self.root)

    def append(self, item: GeneratedFrontMatter):
        """Appends a new GeneratedFrontMatter item to the list."""
        self.root.append(item)
