from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SearchRequest(BaseModel):
    query: str
    year_filter: Optional[str] = None
    category_filter: Optional[str] = None
    author_filter: Optional[str] = None
    title_filter: Optional[str] = None
    abstract_filter: Optional[str] = None
    search_type: str = "manual"  # "manual" or "ai"
    limit: Optional[int] = None

class Article(BaseModel):
    id: int
    title: str
    abstract: str
    published: str
    categories: str
    authors: Optional[str] = None

class SearchResponse(BaseModel):
    articles: List[Article]
    total_count: int
    search_type: str
    explanation: Optional[str] = None

class StatsResponse(BaseModel):
    total_papers: int
    latest_year: str
    year_span: int
    papers_by_year: dict