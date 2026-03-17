"""
report.py — Generates output files from analysis.
Takes analysis dictionary → creates JSON and Markdown files.
No API calls happen here — just file writing.
"""

import json
import os
from datetime import datetime


# ─── File Saving Functions ───────────────────────────────────────────────────

def save_json(analysis: dict) -> str:
    """
    Saves analysis dictionary as JSON file.
    Returns the file path where it was saved.
    """
    os.makedirs("outputs", exist_ok=True)

    file_path = "outputs/analysis.json"

    with open(file_path, "w") as f:
        json.dump(analysis, f, indent=2)

    return file_path


def save_markdown(analysis: dict) -> str:
    """
    Generates markdown report and saves it as .md file.
    Returns the file path where it was saved.
    """
    os.makedirs("outputs", exist_ok=True)

    file_path = "outputs/report.md"

    md_content = generate_markdown(analysis)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    return file_path


# ─── Markdown Generator ──────────────────────────────────────────────────────

def generate_markdown(analysis: dict) -> str:
    """
    Converts analysis dictionary into
    a human readable markdown string.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    scores = analysis["scores"]
    overall = analysis["overall"]
    profile = analysis.get("founder_profile", {})
    problem = analysis["problem_statement"]
    solution = analysis["proposed_solution"]
    innovation = analysis["core_innovation"]
    market = analysis["market_landscape"]
    support = analysis["support_required"]
    tech = analysis["tech_stack"]

    md = f"""# 🚀 Startup Idea Validation Report
Generated: {timestamp}
Founder: {analysis["founder_name"]}
Idea: {analysis["idea_summary"]}

---

## 👤 Founder Profile
- **Name:** {analysis["founder_name"]}
- **Age:** {profile.get("age", "N/A")}
- **Location:** {profile.get("location", "N/A")}
- **Background:** {profile.get("background", "N/A")}
- **Specific Field:** {profile.get("sub_field", "N/A")}
- **Role / Level:** {profile.get("role_level", "N/A")}
- **Skills:** {profile.get("skills", "N/A")}
- **Startup Experience:** {profile.get("startup_exp", "N/A")}
- **Talked to Users:** {profile.get("user_validation", "N/A")}
- **Industry Network:** {profile.get("industry_network", "N/A")}
- **Available Time:** {profile.get("available_time", "N/A")}
- **Main Goal:** {profile.get("main_goal", "N/A")}
- **Motivation:** {profile.get("motivation", "N/A")}
- **Already Tried:** {profile.get("already_tried", "N/A")}
- **Biggest Fear:** {profile.get("biggest_fear", "N/A")}
- **About Themselves:** {profile.get("about_self", "N/A")}

---

## 1️⃣ Problem Statement
- **Description:** {problem["description"]}
- **Target Audience:** {problem["target_audience"]}
- **Why Current Solutions Fail:** {problem["why_current_solutions_fail"]}

---

## 2️⃣ Proposed Solution
- **What is Built:** {solution["what_is_built"]}
- **How it Solves:** {solution["how_it_solves"]}

---

## 3️⃣ Core Innovation
- **Uniqueness:** {innovation["uniqueness"]}
- **Innovation Type:** {innovation["innovation_type"]}

---

## 4️⃣ Market Landscape
- **Similar Solutions:** {market["similar_solutions"]}
- **Competition Level:** {market["competition_level"]}
- **Market Gap:** {market["market_gap"]}

---

## 5️⃣ Scores (1-10)
| Category | Score | Reasoning |
|----------|-------|-----------|
| Market Feasibility | {scores.get("market_feasibility", {}).get("score", "N/A")}/10 | {scores.get("market_feasibility", {}).get("reasoning", "N/A")} |
| Marketing Potential | {scores.get("marketing_potential", {}).get("score", "N/A")}/10 | {scores.get("marketing_potential", {}).get("reasoning", "N/A")} |
| Scalability | {scores.get("scalability", {}).get("score", "N/A")}/10 | {scores.get("scalability", {}).get("reasoning", "N/A")} |
| Revenue Potential | {scores.get("revenue_potential", {}).get("score", "N/A")}/10 | {scores.get("revenue_potential", {}).get("reasoning", "N/A")} |
| Technical Complexity | {scores.get("technical_complexity", {}).get("score", "N/A")}/10 | {scores.get("technical_complexity", {}).get("reasoning", "N/A")} |
| Execution Risk | {scores.get("execution_risk", {}).get("score", "N/A")}/10 | {scores.get("execution_risk", {}).get("reasoning", "N/A")} |

---

## 6️⃣ Support Required
- **Team Needed:** {support["team_needed"]}
- **Funding Stage:** {support["funding_stage"]}
- **Partnerships:** {support["partnerships"]}
- **Regulatory:** {support["regulatory"]}

---

## 7️⃣ Tech Stack
- **Backend:** {tech["backend"]}
- **Frontend:** {tech["frontend"]}
- **Database:** {tech["database"]}
- **Cloud:** {tech["cloud"]}
- **AI Tools:** {tech["ai_tools"]}

---

## 8️⃣ Overall Verdict
- **Overall Score:** {overall["score"]}/10
- **MVP Ready:** {overall["is_mvp_ready"]}
- **Investment Ready:** {overall["is_investment_ready"]}
- **Incubator Ready:** {overall["is_incubator_ready"]}

### Final Verdict
{overall["final_verdict"]}

---
*Report generated by ThynxAI Idea Lab*
"""
    return md