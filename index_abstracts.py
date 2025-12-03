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
    df = pd.read_sql('SELECT id, abstract FROM articles', conn)
    conn.close()
    logging.info(f"Loaded {len(df)} abstracts from arxiv_data.db")

     
    logging.info("Generating embeddings with SentenceTransformer...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    abstracts = df['abstract'].tolist()
    vectors = model.encode(abstracts, show_progress_bar=True)
    logging.info(f"Generated embeddings for {len(vectors)} abstracts")

     
    logging.info("Creating FAISS index...")
    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(vectors))
    logging.info("FAISS index created")

     
    logging.info("Saving FAISS index and article IDs...")
    faiss.write_index(index, 'faiss_index.index')
    df['id'].to_csv('article_ids.csv', index=False)
    logging.info("Abstracts indexed and saved to faiss_index.index and article_ids.csv")
except Exception as e:
    logging.error(f"Error during indexing: {e}")