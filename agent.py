import os
from tavily import TavilyClient

tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


def search_web(query: str) -> dict:
    """Use Tavily to search for election and candidate information."""
    response = tavily.search(
        query=query,
        search_depth="advanced",
        max_results=5,
        include_answer=True,
        topic="news"
    )
    return response


def synthesize_answer(query: str, search_results: dict) -> str:
    """Simple answer using Tavily results (no Gemini)."""
    
    if "answer" in search_results:
        return search_results["answer"]
    
    summaries = []
    for r in search_results.get("results", []):
        summaries.append(f"- {r.get('content', '')}")
    
    return "\n".join(summaries[:5])


def run_agent(query: str) -> dict:
    """Main agent pipeline: search → synthesize → return results."""
    search_results = search_web(query)
    answer = synthesize_answer(query, search_results)

    sources = [
        {"title": r.get("title", "Source"), "url": r.get("url", "")}
        for r in search_results.get("results", [])
    ]

    return {
        "answer": answer,
        "sources": sources,
        "raw_search": search_results
    }