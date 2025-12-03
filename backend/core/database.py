import sqlite3
import pandas as pd
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path: str = "../data/database/arxiv_data.db"):
        self.db_path = db_path
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def get_years(self) -> List[str]:
        """Get all available years from the database."""
        conn = None
        try:
            conn = self.get_connection()
            years_query = "SELECT DISTINCT strftime('%Y', published) as year FROM articles"
            years = pd.read_sql(years_query, conn)['year'].dropna().astype(str).tolist()
            return sorted(list(set(years)), reverse=True)
        except Exception as e:
            logger.error(f"Error getting years: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        conn = None
        try:
            conn = self.get_connection()
            
            # Total papers
            total_papers = pd.read_sql("SELECT COUNT(*) as count FROM articles", conn)['count'].iloc[0]
            
            # Year counts
            year_counts = pd.read_sql("""
                SELECT strftime('%Y', published) as year, COUNT(*) as count 
                FROM articles 
                GROUP BY year 
                ORDER BY year DESC
            """, conn)
            
            return {
                "total_papers": total_papers,
                "latest_year": year_counts['year'].max() if not year_counts.empty else "N/A",
                "year_span": int(year_counts['year'].max()) - int(year_counts['year'].min()) + 1 if not year_counts.empty else 0,
                "papers_by_year": dict(zip(year_counts['year'], year_counts['count']))
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {"total_papers": 0, "latest_year": "N/A", "year_span": 0, "papers_by_year": {}}
        finally:
            if conn:
                conn.close()
    
    def search_articles(self, filters: Dict[str, Any], article_ids: List[int] = None) -> pd.DataFrame:
        """Search articles with filters."""
        conn = None
        try:
            conn = self.get_connection()
            
            sql_query = """
                SELECT DISTINCT a.id
                FROM articles a
                LEFT JOIN article_authors aa ON a.id = aa.article_id
                LEFT JOIN authors au ON aa.author_id = au.id
            """
            conditions = []
            params = []
            
            if filters.get('title_filter'):
                conditions.append("a.title LIKE ?")
                params.append(f"%{filters['title_filter']}%")
            if filters.get('abstract_filter'):
                conditions.append("a.abstract LIKE ?")
                params.append(f"%{filters['abstract_filter']}%")
            if filters.get('author_filter'):
                conditions.append("au.name LIKE ?")
                params.append(f"%{filters['author_filter']}%")
            if filters.get('category_filter'):
                conditions.append("a.categories LIKE ?")
                params.append(f"%{filters['category_filter']}%")
            if filters.get('year_filter') and filters['year_filter'] != 'All':
                conditions.append("strftime('%Y', a.published) = ?")
                params.append(filters['year_filter'])
            
            if article_ids:
                placeholders = ','.join('?' for _ in article_ids)
                conditions.append(f"a.id IN ({placeholders})")
                params.extend(article_ids)
            
            if conditions:
                sql_query += " WHERE " + " AND ".join(conditions)
            
            filtered_df = pd.read_sql_query(sql_query, conn, params=params)
            return filtered_df
            
        except Exception as e:
            logger.error(f"Error searching articles: {e}")
            return pd.DataFrame()
        finally:
            if conn:
                conn.close()
    
    def get_articles_by_ids(self, article_ids: List[int]) -> pd.DataFrame:
        """Get full article details by IDs."""
        if not article_ids:
            logger.warning("No article IDs provided")
            return pd.DataFrame()
            
        conn = None
        try:
            conn = self.get_connection()
            
            placeholders = ','.join('?' for _ in article_ids)
            results_query = f"""
                SELECT a.id, a.title, a.abstract, a.published, a.categories, 
                       GROUP_CONCAT(au.name, '; ') as authors
                FROM articles a
                LEFT JOIN article_authors aa ON a.id = aa.article_id
                LEFT JOIN authors au ON aa.author_id = au.id
                WHERE a.id IN ({placeholders})
                GROUP BY a.id, a.title, a.abstract, a.published, a.categories
                ORDER BY a.published DESC
            """
            
            results = pd.read_sql_query(results_query, conn, params=article_ids)
            return results
            
        except sqlite3.Error as e:
            logger.error(f"Database error getting articles by IDs: {e}")
            return pd.DataFrame()
        except pd.errors.DatabaseError as e:
            logger.error(f"Pandas database error getting articles by IDs: {e}")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Unexpected error getting articles by IDs: {e}")
            return pd.DataFrame()
        finally:
            if conn:
                conn.close()