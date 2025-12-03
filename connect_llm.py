import requests
import json
import re
import logging

 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_KEY = "6abb0367405f002efd4115300d661144aa398d62372a093de50b288bf2a83d44"
class LLMConnect:
    def __init__(self, api_key=API_KEY, api_url="https://api.together.xyz/v1/chat/completions"):
        """Initialize the LLMConnect class with the cloud API endpoint and key."""
        if not api_key:
            raise ValueError("API key is required for cloud LLM connection.")
        self.api_url = api_url
        self.api_key = api_key
        logging.info("LLMConnect initialized for cloud API.")

    def query_llm(self, user_query):
        """Send a query to the cloud LLM API and parse the response."""
        try:
             
            prompt = f"""
You are an AI assistant for an ArXiv research chatbot. The user has asked: "{user_query}"
Your task is to:
1. If the user asks for an explanation (e.g., "What is a neural network?"), provide a concise explanation (100-200 words).
2. Identify search parameters for research papers, including:
   - Search query (e.g., "neural networks")
   - Year filter (e.g., "2025")
   - Category filter (e.g., "cs.AI")
   - Author filter (e.g., "Yann LeCun")
   - Title keywords
   - Abstract keywords
3. Only include filters explicitly mentioned in the query. If a filter is not mentioned, set it to an empty string.
4. Return a JSON object with:
   - "explanation": The explanation text (or empty string if not requested).
   - "search_params": A dictionary with keys "query", "year", "category", "author", "title", "abstract" (use empty strings for unspecified parameters).

Example input: "give me some articles about neural networks"
Example output:
{{
  "explanation": "",
  "search_params": {{
    "query": "neural networks",
    "year": "",
    "category": "",
    "author": "",
    "title": "",
    "abstract": ""
  }}
}}

Example input: "What is a neural network, and give me some articles about it in year 2025 with category cs.AI"
Example output:
{{
  "explanation": "A neural network is a computational model inspired by the human brain, consisting of interconnected nodes (neurons) organized in layers...",
  "search_params": {{
    "query": "neural networks",
    "year": "2025",
    "category": "cs.AI",
    "author": "",
    "title": "",
    "abstract": ""
  }}
}}
"""
             
            payload = {
                "model": "lgai/exaone-3-5-32b-instruct",  
                "messages": [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_query}
                ],
                "max_tokens": 500,
                "temperature": 0.7
            }
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

             
            response = requests.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()

             
            response_text = result["choices"][0]["message"]["content"]
            logging.info("Received response from LLM: %s", response_text)

             
            response_text = re.sub(r'^```json\n|```$', '', response_text, flags=re.MULTILINE).strip()
            try:
                parsed_response = json.loads(response_text)
                return parsed_response
            except json.JSONDecodeError:
                logging.error("Failed to parse LLM response as JSON: %s", response_text)
                 
                search_params = {
                    "query": user_query,
                    "year": "",
                    "category": "",
                    "author": "",
                    "title": "",
                    "abstract": ""
                }
                 
                year_match = re.search(r'\b(20\d{2})\b', user_query)
                if year_match:
                    search_params["year"] = year_match.group(1)
                return {
                    "explanation": "",
                    "search_params": search_params
                }

        except Exception as e:
            logging.error("Error querying LLM: %s", e, exc_info=True)
            return {
                "explanation": "",
                "search_params": {
                    "query": user_query,
                    "year": "",
                    "category": "",
                    "author": "",
                    "title": "",
                    "abstract": ""
                },
                "error": str(e)
            }