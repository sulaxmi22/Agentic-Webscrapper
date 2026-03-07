from pydantic import BaseModel, Field
from typing import Optional, List

class ArticleBaseClass(BaseModel):
    title: str = Field(..., description="The main title of the article")
    articleUrl: str = Field(..., description="The full article URL")  # Changed from HttpUrl to str for Arrow compatibility
    imageUrl: str = Field(..., description="The image URL for the article")  # Changed from HttpUrl to str
    excerpt: str = Field(..., description="A short excerpt of the article")

class ArticleListClass(BaseModel):
    articles: List[ArticleBaseClass] = Field(..., description="List of extracted articles")