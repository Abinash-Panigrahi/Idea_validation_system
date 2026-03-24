"""
websearch.py — Tavily web search integration.
Optimized for high-accuracy RAG context generation.
Location-aware and score-filtered for best results.
"""

import os
import datetime
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


# ─── Core Search Function ─────────────────────────────────────────────────────

def search_web(query: str) -> str:
    """
    Searches the web using Tavily.
    Uses include_answer=True for pre-synthesized accurate summary.
    Score filters low-relevance results before sending to Gemini.
    """
    if client is None:
        print("Tavily not connected. Skipping search.")
        return "No data found (Search disabled)."

    try:
        response = client.search(
            query,
            search_depth="advanced",
            max_results=3,
            include_answer=True,        # Tavily AI synthesizes answer
            include_raw_content=False   # No raw HTML noise
        )

        # 1. Tavily's own AI-generated summary
        ai_answer = response.get("answer", "")

        # 2. Supporting snippets — score filtered for relevance
        snippets = []
        for res in response.get("results", []):
            title = res.get("title", "")
            content = res.get("content", "").replace("\n", " ").strip()
            score = res.get("score", 0)

            # Only use high relevance results
            if score >= 0.5 and len(content) > 50:
                snippets.append(f"- {title}: {content[:250]}...")

        # 3. Clean structured format for Gemini
        if ai_answer:
            final_context = f"SUMMARY:\n{ai_answer}\n\nSOURCES:\n" + "\n".join(snippets)
        else:
            # Fallback if answer is None — use snippets only
            final_context = "SOURCES:\n" + "\n".join(snippets)

        return final_context.strip() if final_context.strip() else "No relevant data found."

    except Exception as e:
        print(f"Search failed: {str(e)}")
        return "No data found due to search error."


# ─── Specific Search Functions ────────────────────────────────────────────────

def search_competitors(idea: str, location: str = "India") -> str:
    query = f"Top startup competitors and alternatives in {location} for this business idea: {idea[:150]}"
    return search_web(query)


def search_market_size(idea: str, location: str = "India") -> str:
    current_year = datetime.datetime.now().year
    query = f"Market size TAM and CAGR growth rate in {location} {current_year} for industry related to: {idea[:150]}"
    return search_web(query)


def search_recent_news(idea: str, location: str = "India") -> str:
    current_year = datetime.datetime.now().year
    query = f"Latest news trends and startup investments in {location} {current_year} for industry related to: {idea[:150]}"
    return search_web(query)


# ─── Combined Search for Analysis ─────────────────────────────────────────────

def get_search_context(idea: str, founder_data: dict = None) -> dict:
    """
    Runs all 3 searches for one idea.
    Uses founder location for targeted results.
    Returns dictionary with all search results.
    """
    # Extract location from founder_data
    location = "India"  # default
    if founder_data:
        raw_location = founder_data.get("location", "India")
        if "," in raw_location:
            location = raw_location.split(",")[-1].strip()
        else:
            location = raw_location
        # Only edge case — user selected "Other"
        if location == "Other":
            location = "Global"

    print(f"🔍 Searching competitors in {location}...")
    competitors = search_competitors(idea, location)

    print(f"🔍 Searching market size in {location}...")
    market_size = search_market_size(idea, location)

    print(f"🔍 Searching recent news in {location}...")
    recent_news = search_recent_news(idea, location)

    return {
        "competitors": competitors,
        "market_size": market_size,
        "recent_news": recent_news
    }