import os
from typing import List
from tavily import TavilyClient
from dotenv import load_dotenv

# Load environment variables (API Keys) securely
load_dotenv()

def execute_web_search(query: str) -> List[str]:
    """
    Executes a real-time web search for the target corporate query
    and returns raw text segments.
    """
    try:
        # Initialize the client using the secured API key
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        
        # Execute deep search optimized for text content extraction
        response = client.search(
            query=query, 
            search_depth="advanced", 
            max_results=5
        )
        
        # Parse the JSON response to extract only the clean text content
        results = []
        for item in response.get("results", []):
            content = item.get("content", "")
            if content:
                results.append(content)
                
        return results

    except Exception as e:
        print(f"Search API Error: {e}")
        return ["Error: Unable to fetch data from the web."]