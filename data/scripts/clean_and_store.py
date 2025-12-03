import pandas as pd
import sqlite3
import logging
import json
import ast

 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

 
category_map = {
    'cs': 'Computer Science',
    'cs.AI': 'Artificial Intelligence',
    'cs.CL': 'Computation and Language',
    'cs.CV': 'Computer Vision and Pattern Recognition',
    'cs.LG': 'Machine Learning',
    'physics': 'Physics',
    'physics.quant-ph': 'Quantum Physics',
    'physics.optics': 'Optics',
    'math': 'Mathematics',
    'math.CO': 'Combinatorics',
    'q-bio': 'Quantitative Biology',
    'q-bio.NC': 'Neurons and Cognition',
    'q-fin': 'Quantitative Finance',
    'stat': 'Statistics',
    'stat.ML': 'Machine Learning',
    'eess': 'Electrical Engineering and Systems Science',
    'econ': 'Economics',
     
}

def convert_categories(categories):
    """Convert category abbreviations to full names."""
    if not isinstance(categories, str) or not categories.strip():
        logging.warning(f"Invalid category format: {categories}, storing as empty")
        return ''
    cats = [cat.strip() for cat in categories.split(',')]
    converted = [category_map.get(cat, cat) for cat in cats]   
    return ', '.join(converted)

try:
     
    logging.info("Reading arxiv_data_raw.csv...")
    df = pd.read_csv('arxiv_data_raw.csv')
    logging.info(f"Loaded {len(df)} papers from arxiv_data_raw.csv")

     
    logging.info("Cleaning data...")
    try:
        df = df.drop_duplicates(subset=['arxiv_id'])
        df['title'] = df['title'].str.strip()
        df['abstract'] = df['abstract'].str.strip()
        df['doi'] = df['doi'].fillna('')
        
        def safe_parse_authors(x):
            if not isinstance(x, str):
                return x
            try:
                return ast.literal_eval(x)
            except (ValueError, SyntaxError):
                logging.warning(f"Failed to parse authors: {x}")
                return []
        
        df['authors'] = df['authors'].apply(safe_parse_authors)
        df['categories'] = df['categories'].apply(convert_categories)
        logging.info(f"After cleaning, {len(df)} unique papers remain")
    except KeyError as e:
        logging.error(f"Missing required column: {e}")
        raise
    except AttributeError as e:
        logging.error(f"Data type error during cleaning: {e}")
        raise

   
    logging.info("Connecting to arxiv_data.db...")
    conn = sqlite3.connect('arxiv_data.db')
    c = conn.cursor()

     
    logging.info("Creating database tables...")
    c.execute('''CREATE TABLE IF NOT EXISTS articles
                 (id INTEGER PRIMARY KEY, arxiv_id TEXT UNIQUE, title TEXT, abstract TEXT, published TEXT, doi TEXT, categories TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS authors
                 (id INTEGER PRIMARY KEY, name TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS article_authors
                 (article_id INTEGER, author_id INTEGER, PRIMARY KEY (article_id, author_id))''')

    def insert_article(conn, article):
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO articles (arxiv_id, title, abstract, published, doi, categories) VALUES (?, ?, ?, ?, ?, ?)',
                  (article['arxiv_id'], article['title'], article['abstract'], article['published'], article['doi'], article['categories']))
        c.execute('SELECT id FROM articles WHERE arxiv_id = ?', (article['arxiv_id'],))
        return c.fetchone()[0]

    def get_or_insert_author(conn, author_name):
        c = conn.cursor()
        c.execute('SELECT id FROM authors WHERE name = ?', (author_name,))
        result = c.fetchone()
        if result:
            return result[0]
        c.execute('INSERT INTO authors (name) VALUES (?)', (author_name,))
        return c.lastrowid

    def insert_article_authors(conn, article_id, authors):
        c = conn.cursor()
        for author_name in authors:
            author_id = get_or_insert_author(conn, author_name)
            c.execute('INSERT OR IGNORE INTO article_authors (article_id, author_id) VALUES (?, ?)',
                      (article_id, author_id))
 
    logging.info("Inserting data into database...")
    batch_size = 100
    for i, (_, row) in enumerate(df.iterrows()):
        article_id = insert_article(conn, row)
        insert_article_authors(conn, article_id, row['authors'])
        
        if (i + 1) % batch_size == 0:
            conn.commit()
            logging.info(f"Processed {i + 1} articles")
    
    conn.commit()  # Final commit for remaining records

    conn.close()
    logging.info("Data cleaned and stored in arxiv_data.db")
except Exception as e:
    logging.error(f"Error during cleaning/storage: {e}")
    if 'conn' in locals():
        conn.close()