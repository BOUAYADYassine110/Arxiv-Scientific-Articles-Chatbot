import requests
import json
import re
import logging
import os

 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_KEY = os.getenv("TOGETHER_API_KEY")
class LLMConnect:
    def __init__(self, api_key=API_KEY, api_url="https://api.together.xyz/v1/chat/completions"):
        """Initialize the LLMConnect class with the cloud API endpoint and key."""
        if not api_key:
            raise ValueError("API key is required for cloud LLM connection. Set TOGETHER_API_KEY environment variable.")
        self.api_url = api_url
        self.api_key = api_key
        logging.info("LLMConnect initialized for cloud API.")

    def query_llm(self, user_query):
        """Send a query to the cloud LLM API and parse the response."""
        try:
             
            prompt = f"""
You are an AI assistant for an ArXiv research chatbot. The user has asked: "{user_query}"
Your task is to:
1. Extract the MAIN TOPIC the user wants to search for (ignore words like "find", "give me", "show me", "papers", "articles", numbers)
2. Extract the result limit if specified (numbers before words like "papers", "articles", "results")
3. Extract other filters if mentioned (year, category, author)
4. If user asks for explanation, provide it

IMPORTANT: The "query" field should contain ONLY the research topic, NOT the full user input.

Examples:
- "find me 10 papers about AI" → query="AI", limit="10"
- "show me 5 articles on neural networks" → query="neural networks", limit="5"
- "give me papers about machine learning in 2024" → query="machine learning", year="2024"
- "I want 20 papers on quantum computing" → query="quantum computing", limit="20"

Return a JSON object with:
- "explanation": Explanation text (or empty string)
- "search_params": Dictionary with "query" (research topic ONLY), "limit", "year", "category", "author", "title", "abstract"

Example 1:
Input: "find me 10 papers about AI"
Output:
{{
  "explanation": "",
  "search_params": {{
    "query": "AI",
    "limit": "10",
    "year": "",
    "category": "",
    "author": "",
    "title": "",
    "abstract": ""
  }}
}}

Example 2:
Input: "show me 5 articles on deep learning"
Output:
{{
  "explanation": "",
  "search_params": {{
    "query": "deep learning",
    "limit": "5",
    "year": "",
    "category": "",
    "author": "",
    "title": "",
    "abstract": ""
  }}
}}

Example 3:
Input: "I need 20 papers on quantum computing from 2024"
Output:
{{
  "explanation": "",
  "search_params": {{
    "query": "quantum computing",
    "limit": "20",
    "year": "2024",
    "category": "",
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
                "max_tokens": 300,
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
                    "limit": "",
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
                    "limit": "",
                    "year": "",
                    "category": "",
                    "author": "",
                    "title": "",
                    "abstract": ""
                },
                "error": str(e)
            }