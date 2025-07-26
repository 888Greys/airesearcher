from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
import os
import json


class SearchToolInput(BaseModel):
    """Input schema for SearchTool."""
    query: str = Field(..., description="The search query to look up on the web.")


class SearchTool(BaseTool):
    name: str = "Web Search"
    description: str = (
        "Useful for searching the web for current information, news, trends, and recent developments. "
        "Use this tool when you need up-to-date information that might not be in your training data. "
        "Provide a clear and specific search query."
    )
    args_schema: Type[BaseModel] = SearchToolInput

    def _run(self, query: str) -> str:
        """
        Perform a web search using SERP API.
        """
        try:
            serp_api_key = os.getenv("SERP_API_KEY")
            if not serp_api_key:
                return "Error: SERP_API_KEY not found in environment variables."
            
            # SERP API endpoint
            url = "https://serpapi.com/search"
            
            params = {
                "q": query,
                "api_key": serp_api_key,
                "engine": "google",
                "num": 10,  # Number of results
                "hl": "en",  # Language
                "gl": "us"   # Country
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract organic results
            results = []
            if "organic_results" in data:
                for result in data["organic_results"][:4]:  # Limit to top 4 results to reduce tokens
                    title = result.get("title", "")
                    snippet = result.get("snippet", "")
                    link = result.get("link", "")
                    
                    results.append(f"**{title}**\n{snippet}\nSource: {link}\n")
            
            # Also check for featured snippets or answer boxes
            if "answer_box" in data:
                answer = data["answer_box"].get("answer", "")
                if answer:
                    results.insert(0, f"**Featured Answer:** {answer}\n")
            
            if "knowledge_graph" in data:
                kg = data["knowledge_graph"]
                title = kg.get("title", "")
                description = kg.get("description", "")
                if title and description:
                    results.insert(0, f"**Knowledge Graph - {title}:** {description}\n")
            
            if not results:
                return f"No search results found for query: {query}"
            
            return f"Search results for '{query}':\n\n" + "\n".join(results)
            
        except requests.exceptions.RequestException as e:
            return f"Error performing web search: {str(e)}"
        except Exception as e:
            return f"Unexpected error during search: {str(e)}"


class NewsSearchTool(BaseTool):
    name: str = "News Search"
    description: str = (
        "Useful for searching recent news articles and current events. "
        "Use this tool when you need the latest news, announcements, or recent developments. "
        "Provide a clear search query related to news or current events."
    )
    args_schema: Type[BaseModel] = SearchToolInput

    def _run(self, query: str) -> str:
        """
        Perform a news search using SERP API.
        """
        try:
            serp_api_key = os.getenv("SERP_API_KEY")
            if not serp_api_key:
                return "Error: SERP_API_KEY not found in environment variables."
            
            # SERP API endpoint for news
            url = "https://serpapi.com/search"
            
            params = {
                "q": query,
                "api_key": serp_api_key,
                "engine": "google",
                "tbm": "nws",  # News search
                "num": 10,
                "hl": "en",
                "gl": "us"
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract news results
            results = []
            if "news_results" in data:
                for result in data["news_results"][:4]:  # Limit to top 4 results to reduce tokens
                    title = result.get("title", "")
                    snippet = result.get("snippet", "")
                    link = result.get("link", "")
                    source = result.get("source", "")
                    date = result.get("date", "")
                    
                    result_text = f"**{title}**"
                    if source:
                        result_text += f" - {source}"
                    if date:
                        result_text += f" ({date})"
                    result_text += f"\n{snippet}\nSource: {link}\n"
                    
                    results.append(result_text)
            
            if not results:
                return f"No news results found for query: {query}"
            
            return f"Latest news for '{query}':\n\n" + "\n".join(results)
            
        except requests.exceptions.RequestException as e:
            return f"Error performing news search: {str(e)}"
        except Exception as e:
            return f"Unexpected error during news search: {str(e)}"