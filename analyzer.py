"""
analyzer.py — Core Gemini API logic.
All API calls live here.
To switch to another LLM — only change this file.
"""

import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from prompts import (
    get_analysis_prompt,
    get_validate_input_prompt,
    get_grade_output_prompt,
    get_adaptive_question_prompt,
    get_readiness_tips_prompt
)
from websearch import get_search_context

load_dotenv()

# ─── Client Setup ───────────────────────────────────────────────────────────

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


# ─── Helper Functions ────────────────────────────────────────────────────────

def clean_json(raw: str) -> str:
    """
    Cleans Gemini response before parsing.
    Gemini sometimes wraps JSON in markdown backticks.
    This function removes them.
    """
    raw = raw.strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1]
        # handles "json", " json", "\njson" all safely
        if raw.lower().lstrip().startswith("json"):
            raw = raw.lstrip()[4:]
    if raw.lower().lstrip().startswith("json"):
        raw = raw.lstrip()[4:]
    return raw.strip()


def call_gemini(prompt: str, max_output_tokens: int = 2048) -> str:
    """
    Core function — every other function calls this.
    Sends prompt to Gemini and returns raw response text.
    """
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                max_output_tokens=max_output_tokens,
                temperature=0.0,
                response_mime_type="application/json"
            )
        )
        return response.text

    except Exception as e:
        raise Exception(f"Gemini API call failed: {str(e)}")
    

def validate_input(idea: str) -> dict:
    prompt = get_validate_input_prompt(idea)
    raw_response = call_gemini(prompt, max_output_tokens=1024)
    cleaned = clean_json(raw_response)
    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"\n⚠️ AI Formatting Error: {e}")
        result = {"status": "INVALID", "reason": "AI formatting failed"}
    return result

def generate_single_question(idea: str, founder_name: str, founder_data: dict, history: list) -> str:
    prompt = get_adaptive_question_prompt(idea, founder_name, founder_data, history)
    raw_response = call_gemini(prompt, max_output_tokens=2048)
    cleaned = clean_json(raw_response)
    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"\n⚠️ AI Formatting Error: {e}")
        print("Raw response:", cleaned[:200])
        result = {"question": "Can you explain more about your target market?"}
    return result.get("question", "Could you tell me a little more about your idea?")

def analyze_idea(idea: str, founder_name: str, founder_data: dict, followup_qa: list) -> dict:
    search_context = get_search_context(idea)
    prompt = get_analysis_prompt(idea, founder_name, founder_data, followup_qa, search_context)
    raw_response = call_gemini(prompt, max_output_tokens=8192)
    cleaned = clean_json(raw_response)
    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"\n⚠️ AI Formatting Error: {e}")
        result = {"error": "Analysis failed. Please try again."}
    return result


def grade_output(analysis: dict) -> dict:
    """
    Grades the quality of the analysis.
    Returns quality score 1-5 with feedback.
    """
    prompt = get_grade_output_prompt(analysis)
    raw_response = call_gemini(prompt, max_output_tokens=1024)
    cleaned = clean_json(raw_response)
    
    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as e:
        # This stops the crash and shows you EXACTLY what the AI did wrong
        print(f"\n⚠️ AI Formatting Error: {e}")
        print("Here is the broken text Gemini tried to send:")
        print("-" * 40)
        print(cleaned)
        print("-" * 40)
        
        # This fallback triggers your automatic retry loop in main.py
        result = {
            "quality_score": 1,
            "feedback": "AI formatting failed, triggering automatic regeneration."
        }
        
    return result

def generate_readiness_tips(analysis: dict, readiness_type: str) -> dict:
    """
    Generates actionable tips to become MVP ready or Investment ready.
    readiness_type = "mvp" or "investment"
    """

    prompt = get_readiness_tips_prompt(analysis, readiness_type)
    raw_response = call_gemini(prompt, max_output_tokens=2048)
    cleaned = clean_json(raw_response)

    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"\n⚠️ AI Formatting Error: {e}")
        print("Raw response:", cleaned[:200])
        result = {
            "what_it_means": "Could not generate tips. Please try again.",
            "why_not_ready": [],
            "steps_to_become_ready": [],
            "realistic_timeline": "N/A",
            "first_action": "Please restart and try again.",
            "what_investors_look_for": []
        }

    return result