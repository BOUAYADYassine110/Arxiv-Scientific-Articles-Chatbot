import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import logging
from typing import List, Dict, Any, Optional
import sys
import os
import re

# Add data/scripts directory to path to import connect_llm
scripts_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'scripts')
sys.path.append(scripts_path)
try:
    from connect_llm import LLMConnect
except ImportError:
    LLMConnect = None

from core.database import DatabaseManager

logger = logging.getLogger(__name__)

class SearchService:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.model = None
        self.index = None
        self.article_ids = None
        self.llm = None
        self._load_resources()
    
    def _load_resources(self):
        """Load FAISS index, model, and article IDs."""
        try:
            # Load FAISS index
            index_path = '../data/indexes/faiss_index.index'
            if not os.path.exists(index_path):
                raise FileNotFoundError(f"FAISS index not found at {index_path}")
            self.index = faiss.read_index(index_path)
            
            # Load article IDs
            csv_path = '../data/database/article_ids.csv'
            if not os.path.exists(csv_path):
                raise FileNotFoundError(f"Article IDs CSV not found at {csv_path}")
            article_ids_df = pd.read_csv(csv_path)
            if 'id' not in article_ids_df.columns:
                raise ValueError("Article IDs CSV missing 'id' column")
            self.article_ids = article_ids_df['id'].tolist()
            
            # Load sentence transformer model
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Initialize LLM if available
            if LLMConnect:
                try:
                    self.llm = LLMConnect()
                except ValueError as e:
                    logger.warning(f"LLM initialization failed: {e}")
                    self.llm = None
            
            logger.info("Resources loaded successfully")
        except FileNotFoundError as e:
            logger.error(f"Resource file not found: {e}")
            raise
        except pd.errors.EmptyDataError as e:
            logger.error(f"CSV file is empty or corrupted: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to load resources: {e}")
            raise
    
    def manual_search(self, query: str, filters: Dict[str, Any], limit: Optional[int] = None) -> Dict[str, Any]:
        """Perform manual search using filters and semantic similarity."""
        try:
            # Get filtered article IDs from database
            filtered_df = self.db_manager.search_articles(filters)
            filtered_ids = set(filtered_df['id'].tolist()) if not filtered_df.empty else set()
            
            # Semantic search if query provided
            final_ids = filtered_ids
            if query and self.model and self.index:
                query_vector = self.model.encode([query])
                D, I = self.index.search(np.array(query_vector), k=200)
                semantic_ids = set(self.article_ids[i] for i in I[0] if i < len(self.article_ids))
                
                if filtered_ids:
                    final_ids = filtered_ids.intersection(semantic_ids)
                else:
                    final_ids = semantic_ids
            
            if not final_ids:
                return {"articles": [], "total_count": 0, "search_type": "manual"}
            
            # Apply limit before fetching full details for performance
            ids_to_fetch = list(final_ids)
            if limit and limit > 0:
                ids_to_fetch = ids_to_fetch[:limit]
            
            # Get full article details
            results = self.db_manager.get_articles_by_ids(ids_to_fetch)
            
            return {
                "articles": results.to_dict('records'),
                "total_count": len(results),
                "search_type": "manual"
            }
        except (AttributeError, ValueError) as e:
            logger.error(f"Invalid search parameters: {e}")
            return {"articles": [], "total_count": 0, "search_type": "manual", "error": "Invalid search parameters"}
        except Exception as e:
            logger.error(f"Error in manual search: {e}")
            return {"articles": [], "total_count": 0, "search_type": "manual", "error": str(e)}
    
    def ai_search(self, query: str, filters: Dict[str, Any], limit: Optional[int] = None) -> Dict[str, Any]:
        """Perform AI-powered search with intelligent query interpretation."""
        try:
            explanation = ""
            
            # Extract limit from query using regex as fallback
            if not limit:
                limit_match = re.search(r'\b(\d+)\s*(?:papers?|articles?|results?)', query.lower())
                if limit_match:
                    limit = int(limit_match.group(1))
                    logger.info(f"Extracted limit from query regex: {limit}")
            
            # Get LLM response
            if self.llm:
                llm_response = self.llm.query_llm(query)
                explanation = llm_response.get("explanation", "")
                search_params = llm_response.get("search_params", {})
                
                # Extract limit from LLM if not already set
                if not limit and search_params.get("limit"):
                    try:
                        limit = int(search_params["limit"])
                        logger.info(f"Extracted limit from LLM: {limit}")
                    except (ValueError, TypeError):
                        pass
                
                # Merge LLM params with user filters (user filters take precedence)
                for key, value in search_params.items():
                    if key != "limit" and key in filters and not filters[key]:
                        filters[key] = value
            
            # Perform enhanced semantic search
            final_ids = set()
            
            if query and self.model and self.index:
                # Try multiple query variations
                queries_to_try = [query]
                if len(query.split()) > 1:
                    important_words = [word for word in query.split() if len(word) > 3]
                    queries_to_try.extend(important_words[:3])
                
                all_semantic_ids = set()
                for search_query in queries_to_try:
                    query_vector = self.model.encode([search_query])
                    D, I = self.index.search(np.array(query_vector), k=150)
                    semantic_ids = set(self.article_ids[i] for i in I[0] if i < len(self.article_ids))
                    all_semantic_ids.update(semantic_ids)
                
                final_ids = all_semantic_ids
            
            # Apply database filters
            if any(filters.values()):
                filtered_df = self.db_manager.search_articles(filters)
                filtered_ids = set(filtered_df['id'].tolist()) if not filtered_df.empty else set()
                
                if final_ids:
                    final_ids = final_ids.intersection(filtered_ids)
                else:
                    final_ids = filtered_ids
            
            if not final_ids:
                return {
                    "articles": [], 
                    "total_count": 0, 
                    "search_type": "ai",
                    "explanation": explanation
                }
            
            # Apply limit before fetching full details for performance
            ids_to_fetch = list(final_ids)
            if limit and limit > 0:
                ids_to_fetch = ids_to_fetch[:limit]
                logger.info(f"Limiting results to {limit} articles")
            
            # Get full article details
            results = self.db_manager.get_articles_by_ids(ids_to_fetch)
            
            return {
                "articles": results.to_dict('records'),
                "total_count": len(results),
                "search_type": "ai",
                "explanation": explanation
            }
        except (AttributeError, ValueError) as e:
            logger.error(f"Invalid AI search parameters: {e}")
            return {
                "articles": [], 
                "total_count": 0, 
                "search_type": "ai", 
                "error": "Invalid search parameters"
            }
        except Exception as e:
            logger.error(f"Error in AI search: {e}")
            return {
                "articles": [], 
                "total_count": 0, 
                "search_type": "ai", 
                "error": str(e)
            }