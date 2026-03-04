"""
prompts.py — All AI prompts are stored here.
Each function builds one specific prompt.
No API calls happen here — just text building.
"""

import json


def get_followup_questions_prompt(idea: str, founder_name: str, background: str) -> str:
    return f"""
<role>
You are an expert startup mentor and investor.
</role>

<founder_info>
Name: {founder_name}
Background: {background}
</founder_info>

<startup_idea>
{idea}
</startup_idea>

<instructions>
Generate exactly 4 intelligent follow-up questions to better understand this idea.
Consider the founder's background:
- If Non-Technical founder → ask about technical team plans
- If Technical founder → ask about business and marketing strategy

Do not use LaTeX or any math notation. Use plain text only.

Respond ONLY in this exact JSON format, no extra text outside JSON:
{{
  "questions": [
    "Question 1?",
    "Question 2?",
    "Question 3?",
    "Question 4?"
  ]
}}
</instructions>
"""


def get_analysis_prompt(idea: str, founder_name: str, background: str, followup_qa: list) -> str:

    qa_text = "\n".join([
        f"Q: {item['question']}\nA: {item['answer']}"
        for item in followup_qa
    ])

    return f"""
<role>
You are a world-class startup analyst and investor.
</role>

<founder_info>
Name: {founder_name}
Background: {background}
</founder_info>

<startup_idea>
{idea}
</startup_idea>

<followup_answers>
{qa_text}
</followup_answers>

<instructions>
Analyze the startup idea considering the founder's background:
- If Non-Technical founder + deep-tech idea → highlight technical team requirement
- If Technical founder + non-tech idea → highlight business execution challenges
- Use language appropriate for a {background} founder. If Non-Technical → avoid jargon, use simple terms. If Technical → use technical terminology where relevant.

Do not use LaTeX or any math notation. Use plain text only.

Respond ONLY in this exact JSON format, no extra text outside JSON:
{{
  "founder_name": "{founder_name}",
  "idea_summary": "one line summary",

  "problem_statement": {{
    "description": "clear description",
    "target_audience": "who faces this problem",
    "why_current_solutions_fail": "why existing solutions are insufficient"
  }},

  "proposed_solution": {{
    "what_is_built": "what exactly is being built",
    "how_it_solves": "how it solves the problem"
  }},

  "core_innovation": {{
    "uniqueness": "what makes it unique",
    "innovation_type": "Technology / Business Model / Both"
  }},

  "market_landscape": {{
    "similar_solutions": "existing competitors",
    "competition_level": "Low / Medium / High",
    "market_gap": "what gap does this fill"
  }},

  "scores": {{
    "market_feasibility": {{"score": 0, "reasoning": "why"}},
    "marketing_potential": {{"score": 0, "reasoning": "why"}},
    "scalability": {{"score": 0, "reasoning": "why"}},
    "revenue_potential": {{"score": 0, "reasoning": "why"}},
    "technical_complexity": {{"score": 0, "reasoning": "why"}},
    "execution_risk": {{"score": 0, "reasoning": "why"}}
  }},

  "support_required": {{
    "team_needed": "type of team",
    "funding_stage": "Bootstrapped / Seed / VC",
    "partnerships": "key partnerships needed",
    "regulatory": "any regulatory considerations"
  }},

  "tech_stack": {{
    "backend": "recommended backend",
    "frontend": "recommended frontend",
    "database": "recommended database",
    "cloud": "recommended cloud",
    "ai_tools": "AI tools if required"
  }},

  "overall": {{
    "score": 0,
    "is_mvp_ready": "Yes / No — explanation",
    "is_investment_ready": "Yes / No — explanation",
    "is_incubator_ready": "Yes / No — explanation",
    "final_verdict": "2-3 sentence overall assessment"
  }}
}}
</instructions>
"""

def get_validate_input_prompt(idea: str) -> str:
    return f"""
<role>
You are a startup idea validator.
</role>

<input>
{idea}
</input>

<instructions>
Think carefully about whether this is a real startup idea.

Rubric:
- If random gibberish or keyboard smashing → INVALID
- If offensive or harmful content → INVALID
- If less than 10 meaningful words → INVALID
- If a real business concept → VALID

Do not use LaTeX or any math notation. Use plain text only.

After thinking, respond ONLY in this exact JSON format:
{{
  "status": "VALID or INVALID",
  "reason": "one line explanation"
}}
</instructions>
"""


def get_grade_output_prompt(analysis: dict) -> str:
    analysis_text = json.dumps(analysis, indent=2)

    return f"""
<role>
You are an expert evaluator of startup analyses.
</role>

<analysis>
{analysis_text}
</analysis>

<instructions>
Think carefully about the quality of this analysis.

Rubric:
- Does it have a clear problem statement?
- Does it have scores with reasoning?
- Does it have a tech stack suggestion?
- Is the overall verdict logical?

Do not use LaTeX or any math notation. Use plain text only.

After thinking, respond ONLY in this exact JSON format:
{{
  "quality_score": 1 to 5,
  "feedback": "one line feedback (integer only for score, no fractions like 4/5)"
}}
</instructions>
"""