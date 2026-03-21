"""
search.py — Tavily web search integration.
All search logic lives here.
To switch to another search API — only change this file.
"""

import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

# ─── Client Setup ─────────────────────────────────────────────────────────────

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

client = None

try:
    if TAVILY_API_KEY:
        client = TavilyClient(api_key=TAVILY_API_KEY)
except Exception as e:
    print(f"Tavily connection failed: {str(e)}")


# ─── Garbage Filter ───────────────────────────────────────────────────────────

BAD_SIGNS = [
    "firewall", "proxy", "Internal Server Error",
    "Ctrl+F5", "Text Size", "Small Medium Large",
    "browser configuration", "click here to retry",
    "hi@tracxn.com", "Press Ctrl"
]

def is_clean(content: str) -> bool:
    """
    Returns True if content is real article text.
    Returns False if content is website UI garbage.
    """
    if len(content) < 100:
        return False
    for sign in BAD_SIGNS:
        if sign in content:
            return False
    return True


# ─── Core Search Function ─────────────────────────────────────────────────────

def search_web(query: str) -> str:
    """
    Searches the web using Tavily.
    Returns clean text ready to inject into Gemini prompt.
    Returns empty string if search fails — never crashes the app.
    """
    if client is None:
        print("Tavily not connected. Skipping search.")
        return ""

    try:
        results = client.search(
            query,
            search_depth="advanced",
            max_results=5
        )

        content_parts = []

        for result in results.get("results", []):
            title = result.get("title", "")
            content = result.get("content", "")
            if is_clean(content):
                content_parts.append(f"{title}:\n{content}")

        return "\n\n".join(content_parts)

    except Exception as e:
        print(f"Search failed: {str(e)}")
        return ""


# ─── Specific Search Functions ────────────────────────────────────────────────

def search_competitors(idea: str) -> str:
    """Finds real competitors for the startup idea."""
    query = f"what are the top competitors and similar startups for {idea[:100]} in India?"
    return search_web(query)


def search_market_size(idea: str) -> str:
    """Finds real market size and growth data."""
    query = f"what is the market size and growth rate of the {idea[:100]} industry in India?"
    return search_web(query)


def search_recent_news(idea: str) -> str:
    """Finds recent news and trends."""
    query = f"what are the latest news and trends in the {idea[:100]} space in 2025?"
    return search_web(query)


# ─── Combined Search for Analysis ─────────────────────────────────────────────

def get_search_context(idea: str) -> dict:
    """
    Runs all 3 searches for one idea.
    Returns dictionary with all search results.
    Called once from analyzer.py before analysis.
    """
    print("🔍 Searching competitors...")
    competitors = search_competitors(idea)

    print("🔍 Searching market size...")
    market_size = search_market_size(idea)

    print("🔍 Searching recent news...")
    recent_news = search_recent_news(idea)

    return {
        "competitors": competitors,
        "market_size": market_size,
        "recent_news": recent_news
    }