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
from prompts import get_pitch_deck_prompt

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

def generate_single_question(idea: str, founder_name: str, founder_data: dict, history: list ,search_context: dict = None) -> str:
    prompt = get_adaptive_question_prompt(idea, founder_name, founder_data, history ,search_context)
    raw_response = call_gemini(prompt, max_output_tokens=4096)
    cleaned = clean_json(raw_response)
    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"\n⚠️ AI Formatting Error: {e}")
        print("Raw response:", cleaned[:200])
        result = {"question": "Can you explain more about your target market?"}
    return result.get("question", "Could you tell me a little more about your idea?")

def analyze_idea(idea: str, founder_name: str, founder_data: dict, followup_qa: list ,search_context: dict = None) -> dict:
    if search_context is None:
        search_context = get_search_context(idea ,founder_data)
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

def generate_readiness_tips(analysis: dict, readiness_type: str ,search_context: dict = None) -> dict:
    """
    Generates actionable tips to become MVP ready or Investment ready.
    readiness_type = "mvp" or "investment"
    """

    prompt = get_readiness_tips_prompt(analysis, readiness_type ,search_context)
    raw_response = call_gemini(prompt, max_output_tokens=4096)
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

def generate_pitch_slides(analysis: dict) -> list:
    import re
    prompt = get_pitch_deck_prompt(analysis)
    
    for attempt in range(3):
        raw_response = call_gemini(prompt, max_output_tokens=4096)
        
        # Extract only the JSON array
        start = raw_response.find("[")
        end = raw_response.rfind("]") + 1
        if start == -1 or end == 0:
            print(f"⚠️ No JSON array found on attempt {attempt+1}")
            continue
        
        content = raw_response[start:end]
        
        # Fix trailing commas before closing brackets/braces
        content = re.sub(r',\s*([\]}])', r'\1', content)
        
        # Remove non-standard control characters
        content = re.sub(r'[\x00-\x1F\x7F]', '', content)
        
        try:
            result = json.loads(content)
            print(f"✅ PPT Generated successfully on attempt {attempt+1}")
            return result
        except json.JSONDecodeError as e:
            print(f"\n⚠️ PPT Generation Error (attempt {attempt+1}): {e}")
            lines = content.splitlines()
            if e.lineno <= len(lines):
                print(f"Context: {lines[e.lineno-1].strip()}")
            continue
    
    print("❌ PPT generation failed after 3 attempts.")
    return []