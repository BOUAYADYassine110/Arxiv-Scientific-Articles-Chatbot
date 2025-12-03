import streamlit as st
import pandas as pd
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging
from connect_llm import LLMConnect   

 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

 
st.set_page_config(
    page_title="ArXiv Research Hub",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

 
if 'search_performed' not in st.session_state:
    st.session_state['search_performed'] = False
if 'dark_mode' not in st.session_state:
    st.session_state['dark_mode'] = True

 
def hex_to_rgb(hex_color):
    """Converts a hex color string to an (r, g, b) tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

 
def apply_custom_css():
    dark_theme = st.session_state.get('dark_mode', True)
    
    if dark_theme:
        primary_bg = "#0E1117"
        secondary_bg = "#1E2329"
        card_bg = "#262730"
        text_color = "#FAFAFA"
        accent_color = "#FF6B6B"
        gradient_start = "#667eea"
        gradient_end = "#764ba2"
        border_color = "#404040"
    else:
        primary_bg = "#DFCCCCB7"
        secondary_bg = "#8F9398"
        card_bg = "#FFFFFF"
        text_color = "#2C3E50"
        accent_color = "#3498DB"
        gradient_start = "#74b9ff"
        gradient_end = "#0984e3"
        border_color = "#E9ECEF"

    text_color_rgb = hex_to_rgb(text_color)

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {{
        background: {primary_bg};
        font-family: 'Inter', sans-serif;
    }}
    
    /* Hide default elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Hero Section */
    .hero-container {{
        background: linear-gradient(135deg, {gradient_start} 0%, {gradient_end} 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }}
    
    .hero-container::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); opacity: 0.5; }}
        50% {{ transform: scale(1.1); opacity: 0.8; }}
    }}
    
    .hero-title {{
        font-size: 3.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }}
    
    .hero-subtitle {{
        font-size: 1.2rem;
        color: rgba(255,255,255,0.9);
        margin-bottom: 0;
        position: relative;
        z-index: 1;
    }}
    
    /* Search Section */
    .search-container {{
        background: {card_bg};
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid {border_color};
    }}
    
    .search-title {{
        color: {text_color};
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    
    /* Custom Input Styles */
    .stTextInput > div > div > input {{
        background: {secondary_bg};
        border: 2px solid {border_color};
        border-radius: 12px;
        padding: 1rem;
        font-size: 1rem;
        color: {text_color};
        transition: all 0.3s ease;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {accent_color};
        box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
    }}
    
    .stSelectbox > div > div > select {{
        background: {secondary_bg};
        border: 2px solid {border_color};
        border-radius: 12px;
        padding: 1rem;
        color: {text_color};
    }}
    
    /* Modern Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, {accent_color} 0%, {gradient_end} 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        width: 100%;
        position: relative;
        overflow: hidden;
    }}
    
    .stButton > button::before {{
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255,255,255,0.2);
        border-radius: 50%;
        transition: all 0.5s ease;
        transform: translate(-50%, -50%);
    }}
    
    .stButton > button:hover::before {{
        width: 300px;
        height: 300px;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }}
    
    /* Filter Section */
    .filter-section {{
        background: {card_bg};
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid {border_color};
    }}
    
    .filter-title {{
        color: {text_color};
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    
    /* Applied Filters Display */
    .applied-filters {{
        background: linear-gradient(135deg, rgba(74, 144, 226, 0.1) 0%, rgba(76, 201, 240, 0.1) 100%);
        border: 2px solid {accent_color};
        border-radius: 16px;
        padding: 1.5rem;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
    }}
    
    .applied-filters::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, {accent_color} 0%, {gradient_end} 100%);
    }}
    
    .applied-filters h4 {{
        color: {text_color};
        margin-bottom: 1rem;
        font-weight: 600;
    }}
    
    .applied-filters ul {{
        list-style: none;
        padding: 0;
        margin: 0;
    }}
    
    .applied-filters li {{
        color: {text_color};
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(74, 144, 226, 0.2);
    }}
    
    .applied-filters li:last-child {{
        border-bottom: none;
    }}
    
    /* Results Cards */
    .result-card {{
        background: {card_bg};
        border: 1px solid {border_color};
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .result-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, {accent_color} 0%, {gradient_end} 100%);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }}
    
    .result-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }}
    
    .result-card:hover::before {{
        transform: scaleX(1);
    }}
    
    .result-card h4 {{
        color: {text_color};
        margin-bottom: 1rem;
        font-weight: 600;
        line-height: 1.3;
    }}
    
    .result-card p {{
        color: {text_color};
        margin-bottom: 0.8rem;
        line-height: 1.6;
    }}
    
    .result-card .abstract {{
        color: rgba({text_color_rgb[0]}, {text_color_rgb[1]}, {text_color_rgb[2]}, 0.8);
        font-style: italic;
    }}
    
    /* Metrics Cards */
    .metric-card {{
        background: {card_bg};
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        border: 1px solid {border_color};
        transition: all 0.3s ease;
    }}
    
    .metric-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }}
    
    .metric-number {{
        font-size: 2.5rem;
        font-weight: 700;
        color: {accent_color};
        margin-bottom: 0.5rem;
    }}
    
    .metric-label {{
        color: {text_color};
        font-size: 1rem;
        font-weight: 500;
    }}
    
    /* Sidebar Styling */
    .css-1d391kg {{
        background: {secondary_bg};
    }}
    
    .css-1d391kg .stSelectbox > div > div > select {{
        background: {card_bg};
        color: {text_color};
    }}
    
    /* Loading Animation */
    .loading {{
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }}
    
    .spinner {{
        width: 40px;
        height: 40px;
        border: 4px solid {border_color};
        border-top: 4px solid {accent_color};
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }}
    
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    
    /* Responsive Design */
    @media (max-width: 768px) {{
        .hero-title {{
            font-size: 2.5rem;
        }}
        
        .hero-subtitle {{
            font-size: 1rem;
        }}
        
        .search-container, .filter-section {{
            padding: 1.5rem;
        }}
        
        .result-card {{
            padding: 1.5rem;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

 
@st.cache_resource
def load_resources():
    """Loads all necessary resources, cached for performance."""
    logging.info("Loading resources...")
    try:
        index = faiss.read_index('faiss_index.index')
        article_ids = pd.read_csv('article_ids.csv')['id'].tolist()
        model = SentenceTransformer('all-MiniLM-L6-v2')
        logging.info("Resources loaded successfully.")
        return index, article_ids, model
    except Exception as e:
        st.error(f"Failed to load resources: {e}")
        return None, None, None

 
apply_custom_css()

 
def main():
     
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title"> ArXiv Research Hub</div>
        <div class="hero-subtitle">Discover and explore 4,000+ research papers with AI-powered search</div>
    </div>
    """, unsafe_allow_html=True)
    
     
    with st.sidebar:
        st.markdown("###  Settings")
        if st.button(" Toggle Theme"):
            st.session_state['dark_mode'] = not st.session_state['dark_mode']
            st.rerun()
        
        st.markdown(" Quick Stats")
         
    
    try:
         
        with st.spinner("Loading AI models and data..."):
            index, article_ids, model = load_resources()
            
        if index is None:
            st.error("Failed to load required resources. Please check your data files.")
            return
            
        conn = sqlite3.connect('arxiv_data.db')
        llm = LLMConnect()
        
         
        years_query = "SELECT DISTINCT strftime('%Y', published) as year FROM articles"
        years = pd.read_sql(years_query, conn)['year'].dropna().astype(str).tolist()
        years = sorted(list(set(years)), reverse=True)
        
        
        st.markdown("""
        <div class="search-container">
            <div class="search-title"> Search Query</div>
        </div>
        """, unsafe_allow_html=True)
        
        
        query = st.text_input(
            'Search query',  
            placeholder='Enter your research question or keywords (e.g., "neural networks for computer vision")',
            help="Use natural language to describe what you're looking for",
            label_visibility="hidden"  
        )
        
         
        st.markdown("""
        <div class="filter-section">
            <div class="filter-title"> Advanced Filters</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            category_filter = st.text_input(' Category', placeholder='e.g., cs.AI, stat.ML')
            title_filter = st.text_input(' Title Keywords', placeholder='e.g., transformer, neural')
        
        with col2:
            author_filter = st.text_input(' Author', placeholder='e.g., Yann LeCun')
            abstract_filter = st.text_input(' Abstract Keywords', placeholder='e.g., deep learning')
        
        with col3:
            year_filter = st.selectbox(' Publication Year', ['All'] + years)
            st.write("")   
        
         
        col_search, col_ai, col_clear = st.columns([1, 1, 1])
        
        with col_search:
            manual_search_clicked = st.button(" Manual Search", help="Search using filters and semantic similarity")
        
        with col_ai:
            ai_search_clicked = st.button(" AI Search", help="Let AI understand your query and search intelligently")
        
        with col_clear:
            if st.button(" Clear All", help="Clear all filters and start fresh"):
                st.rerun()
        
        
        if manual_search_clicked:
            if not query and not any([category_filter, author_filter, title_filter, abstract_filter, year_filter != 'All']):
                st.warning(" Please enter a search query or apply at least one filter for manual search.")
                return
            
            with st.spinner(" Performing manual search..."):
                results = perform_manual_search(
                    query, year_filter, category_filter, 
                    author_filter, title_filter, abstract_filter, 
                    conn, index, article_ids, model
                )
                
                if results is not None and len(results) > 0:
                    st.success(f" Found {len(results)} papers using manual search")
                    display_results(results, search_type="Manual")
                else:
                    st.warning(" No papers found matching your criteria. Try broadening your search.")
        
         
        if ai_search_clicked:
            if not query:
                st.warning(" Please enter a question or description for AI search.")
                return
            
            with st.spinner(" AI is analyzing your query and searching..."):
                try:
                    
                    llm_response = llm.query_llm(query)
                    explanation = llm_response.get("explanation", "")
                    search_params = llm_response.get("search_params", {})
                    
                    if explanation:
                        st.markdown(" AI Assistant Response")
                        st.info(explanation)
                    
                     
                    search_query = search_params.get("query", query)
                    search_year = year_filter if year_filter != 'All' else search_params.get("year", "")
                    search_category = category_filter if category_filter else search_params.get("category", "")
                    search_author = author_filter if author_filter else search_params.get("author", "")
                    search_title = title_filter if title_filter else search_params.get("title", "")
                    search_abstract = abstract_filter if abstract_filter else search_params.get("abstract", "")
                    
                    results = perform_ai_search(
                        search_query, search_year, search_category, 
                        search_author, search_title, search_abstract, 
                        conn, index, article_ids, model
                    )
                    
                    if results is not None and len(results) > 0:
                        st.success(f" AI found {len(results)} relevant papers")
                        display_results(results, search_type="AI")
                    else:
                        st.warning("AI couldn't find papers matching your query. Try rephrasing your question.")
                
                except Exception as e:
                    st.error(f" AI search failed: {str(e)}")
                    st.info(" Try using manual search instead.")
        
         
        if not st.session_state.get('search_performed', False):
            display_global_stats(conn)
        
        conn.close()
        
    except Exception as e:
        st.error(f"An error occurred: {e}")
        logging.error(f"Error in main app: {e}", exc_info=True)

def perform_manual_search(query, year_filter, category_filter, author_filter, title_filter, abstract_filter, conn, index, article_ids, model):
    """Manual search using direct filters and semantic similarity."""
    st.session_state['search_performed'] = True
    
     
    display_applied_filters(query, year_filter, category_filter, author_filter, title_filter, abstract_filter, "Manual Search")
    
     
    sql_query = """
        SELECT DISTINCT a.id
        FROM articles a
        LEFT JOIN article_authors aa ON a.id = aa.article_id
        LEFT JOIN authors au ON aa.author_id = au.id
    """
    conditions = []
    params = []
    
    if title_filter:
        conditions.append("a.title LIKE ?")
        params.append(f"%{title_filter}%")
    if abstract_filter:
        conditions.append("a.abstract LIKE ?")
        params.append(f"%{abstract_filter}%")
    if author_filter:
        conditions.append("au.name LIKE ?")
        params.append(f"%{author_filter}%")
    if category_filter:
        conditions.append("a.categories LIKE ?")
        params.append(f"%{category_filter}%")
    if year_filter and year_filter != 'All':
        conditions.append("strftime('%Y', a.published) = ?")
        params.append(year_filter)
    
    if conditions:
        sql_query += " WHERE " + " AND ".join(conditions)
    
     
    filtered_df = pd.read_sql_query(sql_query, conn, params=params)
    filtered_ids = set(filtered_df['id'].tolist())
    
    
    final_ids = filtered_ids
    if query:
        query_vector = model.encode([query])
        D, I = index.search(np.array(query_vector), k=202)   
        semantic_ids = set(article_ids[i] for i in I[0])
        
         
        if conditions:
            final_ids = filtered_ids.intersection(semantic_ids)
        else:
            final_ids = semantic_ids
     
    if not final_ids:
        return None
    
    return get_final_results(final_ids, conn)

def perform_ai_search(query, year_filter, category_filter, author_filter, title_filter, abstract_filter, conn, index, article_ids, model):
    """AI-powered search with intelligent query interpretation."""
    st.session_state['search_performed'] = True
    
    
    display_applied_filters(query, year_filter, category_filter, author_filter, title_filter, abstract_filter, "AI Search")
    
     
    final_ids = set()
    
    if query:
        
        queries_to_try = [query]
        
        
        if len(query.split()) > 1:
             
            important_words = [word for word in query.split() if len(word) > 3]
            queries_to_try.extend(important_words[:3])   
        
        all_semantic_ids = set()
        
        for search_query in queries_to_try:
            query_vector = model.encode([search_query])
            D, I = index.search(np.array(query_vector), k=150)
            semantic_ids = set(article_ids[i] for i in I[0])
            all_semantic_ids.update(semantic_ids)
        
        final_ids = all_semantic_ids
    
     
    if any([year_filter, category_filter, author_filter, title_filter, abstract_filter]):
        sql_query = """
            SELECT DISTINCT a.id
            FROM articles a
            LEFT JOIN article_authors aa ON a.id = aa.article_id
            LEFT JOIN authors au ON aa.author_id = au.id
        """
        conditions = []
        params = []
        
        if title_filter:
            conditions.append("a.title LIKE ?")
            params.append(f"%{title_filter}%")
        if abstract_filter:
            conditions.append("a.abstract LIKE ?")
            params.append(f"%{abstract_filter}%")
        if author_filter:
            conditions.append("au.name LIKE ?")
            params.append(f"%{author_filter}%")
        if category_filter:
            conditions.append("a.categories LIKE ?")
            params.append(f"%{category_filter}%")
        if year_filter and year_filter != 'All':
            conditions.append("strftime('%Y', a.published) = ?")
            params.append(year_filter)
        
        if conditions:
            sql_query += " WHERE " + " AND ".join(conditions)
            
            filtered_df = pd.read_sql_query(sql_query, conn, params=params)
            filtered_ids = set(filtered_df['id'].tolist())
            
             
            if final_ids:
                final_ids = final_ids.intersection(filtered_ids)
            else:
                final_ids = filtered_ids
    
    if not final_ids:
        return None
    
    return get_final_results(final_ids, conn)

def get_final_results(final_ids, conn):
    """Get final formatted results from article IDs."""
    final_ids_list = list(final_ids)
    placeholders = ','.join('?' for _ in final_ids_list)
    
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
    
    results = pd.read_sql_query(results_query, conn, params=final_ids_list)
    return results

def display_applied_filters(query, year_filter, category_filter, author_filter, title_filter, abstract_filter, search_type="Search"):
    """Display applied filters in a beautiful format."""
    filters = []
    if query:
        filters.append(f"<strong>Query:</strong> {query}")
    if year_filter and year_filter != 'All':
        filters.append(f"<strong>Year:</strong> {year_filter}")
    if category_filter:
        filters.append(f"<strong>Category:</strong> {category_filter}")
    if author_filter:
        filters.append(f"<strong>Author:</strong> {author_filter}")
    if title_filter:
        filters.append(f"<strong>Title Keywords:</strong> {title_filter}")
    if abstract_filter:
        filters.append(f"<strong>Abstract Keywords:</strong> {abstract_filter}")
    
    if filters:
        filter_html = "<br>".join(f"<li>{f}</li>" for f in filters)
        search_icon = "🤖" if search_type == "AI Search" else "🔍"
        st.markdown(f"""
        <div class="applied-filters">
            <h4>{search_icon} {search_type} - Applied Filters</h4>
            <ul>{filter_html}</ul>
        </div>
        """, unsafe_allow_html=True)

def display_results(results, search_type="Search"):
    """Display search results with enhanced formatting."""
    search_icon = "🤖" if search_type == "AI" else "🔍"
    st.markdown(f"### {search_icon} {search_type} Results")
    
    # Results metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{len(results)}</div>
            <div class="metric-label">Papers Found</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        unique_authors = results['authors'].str.split('; ').explode().nunique()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{unique_authors}</div>
            <div class="metric-label">Unique Authors</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        year_range = results['published'].apply(lambda x: pd.to_datetime(x).year)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{year_range.max() - year_range.min() + 1}</div>
            <div class="metric-label">Year Span</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
     
    for idx, row in results.iterrows():
         
        abstract = row['abstract']
        if len(abstract) > 400:
            abstract = abstract[:400] + "..."
        
         
        authors = row['authors'] if row['authors'] else "Unknown"
        if len(authors) > 100:
            authors = authors[:100] + "..."
        
        
        pub_date = pd.to_datetime(row['published']).strftime('%B %d, %Y')
        
        
        type_badge = " AI" if search_type == "AI" else " Manual"
        
        st.markdown(f"""
        <div class="result-card">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                <h4 style="margin: 0; flex-grow: 1;">{row['title']}</h4>
                <span style="background: rgba(74, 144, 226, 0.2); padding: 4px 8px; border-radius: 12px; font-size: 0.8em; margin-left: 10px;">{type_badge}</span>
            </div>
            <p class="abstract"><strong>Abstract:</strong> {abstract}</p>
            <p><strong>Authors:</strong> {authors}</p>
            <p><strong>Published:</strong> {pub_date}</p>
            <p><strong>Categories:</strong> {row.get('categories', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
    
     
    display_visualizations(results, search_type)

def display_visualizations(results, search_type):
    """Create beautiful visualizations for the results."""
    st.markdown(" Results Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        
        results['year'] = pd.to_datetime(results['published']).dt.year
        year_counts = results['year'].value_counts().sort_index()
        
        fig_year = px.bar(
            x=year_counts.index,
            y=year_counts.values,
            title="Publications by Year",
            labels={'x': 'Year', 'y': 'Number of Papers'},
            color=year_counts.values,
            color_continuous_scale='Plasma'
        )
        fig_year.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white' if st.session_state.get('dark_mode', True) else 'black')
        )
        st.plotly_chart(fig_year, use_container_width=True)
    
    with col2:
         
        if results['categories'].notnull().any():
            cat_series = results['categories'].str.split(r'[\s;]+').explode().str.strip()
            cat_counts = cat_series.value_counts().head(10)
            
            fig_cat = px.pie(
                values=cat_counts.values,
                names=cat_counts.index,
                title="Top Categories",
                color_discrete_sequence=px.colors.qualitative.G10
            )
            fig_cat.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white' if st.session_state.get('dark_mode', True) else 'black')
            )
            st.plotly_chart(fig_cat, use_container_width=True)

def display_global_stats(conn):
    """Display global database statistics."""
    st.markdown("Database Overview")
    
     
    total_papers = pd.read_sql("SELECT COUNT(*) as count FROM articles", conn)['count'].iloc[0]
    
     
    year_counts = pd.read_sql("""
        SELECT strftime('%Y', published) as year, COUNT(*) as count 
        FROM articles 
        GROUP BY year 
        ORDER BY year DESC
    """, conn)
    
     
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{total_papers:,}</div>
            <div class="metric-label">Total Papers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        latest_year = year_counts['year'].max()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{latest_year}</div>
            <div class="metric-label">Latest Year</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        year_span = int(year_counts['year'].max()) - int(year_counts['year'].min()) + 1
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{year_span}</div>
            <div class="metric-label">Years Covered</div>
        </div>
        """, unsafe_allow_html=True)
    
    
    fig = px.bar(
        year_counts,
        x='year',
        y='count',
        title='All Papers by Publication Year',
        labels={'year': 'Year', 'count': 'Number of Papers'},
        color='count',
        color_continuous_scale='Plasma'
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white' if st.session_state.get('dark_mode', True) else 'black')
    )
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()