from fastapi import APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import SearchRequest, SearchResponse, StatsResponse
from services.search_service import SearchService
from core.database import DatabaseManager
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
search_service = SearchService()
db_manager = DatabaseManager()

@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get database statistics."""
    try:
        stats = db_manager.get_stats()
        return StatsResponse(**stats)
    except Exception as e:
        logger.error(f"Failed to retrieve statistics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve statistics")

@router.get("/years")
async def get_years():
    """Get available years."""
    try:
        years = db_manager.get_years()
        return {"years": years}
    except Exception as e:
        logger.error(f"Failed to retrieve years: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve years")

@router.post("/search", response_model=SearchResponse)
async def search_articles(request: SearchRequest):
    """Search articles using manual or AI search."""
    try:
        filters = {
            "year_filter": request.year_filter,
            "category_filter": request.category_filter,
            "author_filter": request.author_filter,
            "title_filter": request.title_filter,
            "abstract_filter": request.abstract_filter
        }
        
        # Extract limit from LLM response if AI search and no explicit limit
        limit = request.limit
        if request.search_type == "ai" and not limit:
            # AI search will handle limit extraction from LLM response
            pass
        
        if request.search_type == "ai":
            result = search_service.ai_search(request.query, filters, limit)
        else:
            result = search_service.manual_search(request.query, filters, limit)
        
        return SearchResponse(**result)
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while searching articles")