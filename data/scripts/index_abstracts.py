import pandas as pd
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import logging

 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
     
    logging.info("Connecting to arxiv_data.db...")
    conn = sqlite3.connect('arxiv_data.db')
    df = pd.read_sql('SELECT id, abstract FROM articles WHERE abstract IS NOT NULL AND abstract != ""', conn)
    conn.close()
    
    if df.empty:
        raise ValueError("No valid abstracts found in database")
    
    logging.info(f"Loaded {len(df)} valid abstracts from arxiv_data.db")

     
    logging.info("Generating embeddings with SentenceTransformer...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Validate and sanitize abstracts
    abstracts = []
    valid_ids = []
    for idx, row in df.iterrows():
        abstract = str(row['abstract']).strip()
        if len(abstract) > 10:  # Minimum length validation
            abstracts.append(abstract[:5000])  # Truncate to prevent memory issues
            valid_ids.append(row['id'])
    
    if not abstracts:
        raise ValueError("No valid abstracts after filtering")
    
    vectors = model.encode(abstracts, show_progress_bar=True, normalize_embeddings=True)
    logging.info(f"Generated normalized embeddings for {len(vectors)} abstracts")

     
    logging.info("Creating FAISS index...")
    dimension = vectors.shape[1]
    index = faiss.IndexFlatIP(dimension)  # Use inner product for normalized vectors
    index.add(np.array(vectors, dtype=np.float32))
    logging.info("FAISS index created")

     
    logging.info("Saving FAISS index and article IDs...")
    import os
    os.makedirs('../indexes', exist_ok=True)
    faiss.write_index(index, '../indexes/faiss_index.index')
    pd.DataFrame({'id': valid_ids}).to_csv('../database/article_ids.csv', index=False)
    logging.info("Abstracts indexed and saved to ../indexes/faiss_index.index and ../database/article_ids.csv")
except ValueError as e:
    logging.error(f"Data validation error: {e}")
except MemoryError as e:
    logging.error(f"Memory error during embedding generation: {e}")
except Exception as e:
    logging.error(f"Error during indexing: {e}")
    raise