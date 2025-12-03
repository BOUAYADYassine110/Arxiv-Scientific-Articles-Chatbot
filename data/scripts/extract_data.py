import arxiv
import pandas as pd
import logging
import csv
from datetime import datetime
import time

 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='extract_data.log')

 
start_date = datetime(2020, 1, 1)
end_date = datetime(2025, 6, 27)   
max_results_per_category = 1000   

 
categories = [
    'cs', 'physics', 'math', 'q-bio', 'q-fin', 'stat', 'eess', 'econ',
    'cs.AI', 'cs.CL', 'cs.CV', 'cs.LG', 'physics.quant-ph', 'math.CO'
     
]

all_papers = []

try:
    logging.info(f"Starting data extraction for {len(categories)} categories from {start_date.date()} to {end_date.date()}...")
    for category in categories:
        try:
            logging.info(f"Fetching papers for category: {category}")
            try:
                search = arxiv.Search(
                    query=f"cat:{category}",
                    max_results=max_results_per_category,
                    sort_by=arxiv.SortCriterion.SubmittedDate,
                    iterative=True,
                    created__gte=start_date,
                    created__lte=end_date
                )
            except ValueError as e:
                logging.error(f"Invalid search parameters for category {category}: {e}")
                continue
            
            papers = []
            try:
                for result in search.results():
                    paper = {
                        'arxiv_id': result.entry_id.split('/')[-1],
                        'title': result.title,
                        'abstract': result.summary,
                        'published': result.published.date().isoformat(),
                        'doi': result.doi if result.doi else '',
                        'authors': [author.name for author in result.authors],
                        'categories': ', '.join(result.categories)   
                    }
                    papers.append(paper)
            except AttributeError as e:
                logging.error(f"Missing result attribute for category {category}: {e}")
                continue
            
            all_papers.extend(papers)
            logging.info(f"Fetched {len(papers)} papers for category {category}")
        except (ConnectionError, TimeoutError) as e:
            logging.error(f"Network error for category {category}: {e}")
            continue
        except arxiv.ArxivError as e:
            logging.error(f"ArXiv API error for category {category}: {e}")
            continue
        except Exception as e:
            logging.error(f"Unexpected error for category {category}: {e}")
            continue

    if not all_papers:
        raise ValueError("No papers were successfully extracted")
     
    df = pd.DataFrame(all_papers)
    df.to_csv('arxiv_data_raw.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)
    logging.info(f"Extracted and saved {len(df)} papers to arxiv_data_raw.csv")
except ValueError as e:
    logging.error(f"Data validation error: {e}")
except PermissionError as e:
    logging.error(f"File permission error: {e}")
except Exception as e:
    logging.error(f"Error during extraction: {e}")