"""
search.py - Tavily API integration for real-time web search
Retrieves trusted and recent sources for fact-checking claims.
"""

import os
from typing import Optional
from tavily import TavilyClient


def search_claim(claim: str, max_results: int = 8) -> dict:
    """
    Search the web for evidence related to a claim using Tavily API.

    Args:
        claim: The claim or statement to search for
        max_results: Maximum number of results to retrieve

    Returns:
        dict with 'results' (list of sources) and 'answer' (AI summary)
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY not found in environment variables.")

    client = TavilyClient(api_key=api_key)

    try:
        response = client.search(
            query=claim,
            search_depth="advanced",
            max_results=max_results,
            include_answer=True,
            include_raw_content=False,
            include_images=False,
        )

        results = []
        for item in response.get("results", []):
            results.append({
                "title": item.get("title", "No Title"),
                "url": item.get("url", ""),
                "content": item.get("content", ""),
                "score": item.get("score", 0),
                "published_date": item.get("published_date", "Unknown"),
            })

        return {
            "results": results,
            "answer": response.get("answer", ""),
            "query": claim,
        }

    except Exception as e:
        raise RuntimeError(f"Tavily search failed: {str(e)}")


def format_search_results(search_data: dict) -> str:
    """
    Format search results into a readable string for the AI prompt.

    Args:
        search_data: Dictionary containing search results

    Returns:
        Formatted string of search evidence
    """
    if not search_data.get("results"):
        return "No search results found."

    formatted = []

    if search_data.get("answer"):
        formatted.append(f"Web Summary: {search_data['answer']}\n")

    formatted.append("=== SEARCH EVIDENCE ===\n")

    for i, result in enumerate(search_data["results"], 1):
        formatted.append(f"[Source {i}]")
        formatted.append(f"Title: {result['title']}")
        formatted.append(f"URL: {result['url']}")
        formatted.append(f"Content: {result['content'][:500]}...")
        if result.get("published_date") and result["published_date"] != "Unknown":
            formatted.append(f"Published: {result['published_date']}")
        formatted.append("")

    return "\n".join(formatted)
