"""
app.py — Streamlit UI for ThynxAI Idea Lab
Run with: streamlit run app.py
"""

import streamlit as st
from analyzer import (
    validate_input,
    generate_followup_questions,
    analyze_idea,
    grade_output
)
from report import save_json, save_markdown


# ─── Page Config ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="ThynxAI Idea Lab",
    page_icon="🚀",
    layout="centered"
)


# ─── Title ───────────────────────────────────────────────────────────────────

st.title("🚀 ThynxAI Idea Lab")
st.subheader("AI-Powered Startup Idea Validator")
st.divider()


# ─── Sidebar ─────────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("📌 About")
    st.write("This tool analyzes your startup idea using AI.")
    st.divider()
    st.write("**How it works:**")
    st.write("1. Describe your idea")
    st.write("2. Tell us about yourself")
    st.write("3. Answer follow-up questions")
    st.write("4. Get full analysis report")
    st.divider()
    st.write("Built with Gemini AI + Python")


# ─── Session State ────────────────────────────────────────────────────────────

if "step" not in st.session_state:
    st.session_state.step = 1

if "idea" not in st.session_state:
    st.session_state.idea = ""

if "founder_name" not in st.session_state:
    st.session_state.founder_name = ""

if "background" not in st.session_state:
    st.session_state.background = ""

if "questions" not in st.session_state:
    st.session_state.questions = []

if "followup_qa" not in st.session_state:
    st.session_state.followup_qa = []

if "analysis" not in st.session_state:
    st.session_state.analysis = None


# ─── Step 1: Idea Input ───────────────────────────────────────────────────────

if st.session_state.step == 1:
    st.header("📝 Step 1: Describe Your Startup Idea")
    st.divider()

    idea = st.text_area(
        "Please describe your startup idea in detail:",
        height=150,
        placeholder="e.g. An AI app that helps restaurants reduce food waste..."
    )

    if st.button("Next →", key="btn_step1"):
        if not idea.strip():
            st.error("❌ Please enter your startup idea first!")
        else:
            with st.spinner("⏳ Validating your idea..."):
                validation = validate_input(idea)

            if validation["status"] == "INVALID":
                st.error(f"❌ {validation['reason']}")
            else:
                st.session_state.idea = idea
                st.session_state.step = 2
                st.rerun()


# ─── Step 2: Founder Information ─────────────────────────────────────────────

if st.session_state.step == 2:
    st.header("👤 Step 2: Tell Us About Yourself")
    st.divider()

    founder_name = st.text_input(
        "What is your name?",
        placeholder="e.g. Rahul"
    )

    background = st.radio(
        "What is your background?",
        options=["Technical", "Non-Technical", "Other"]
    )

    if st.button("Next →", key="btn_step2"):
        if not founder_name.strip():
            st.error("❌ Please enter your name!")
        else:
            st.session_state.founder_name = founder_name
            st.session_state.background = background
            st.session_state.step = 3
            st.rerun()


# ─── Step 3: Follow-up Questions ─────────────────────────────────────────────

if st.session_state.step == 3:
    st.header("❓ Step 3: Follow-up Questions")
    st.divider()

    if not st.session_state.questions:
        with st.spinner("⏳ Generating questions based on your idea..."):
            questions = generate_followup_questions(
                st.session_state.idea,
                st.session_state.founder_name,
                st.session_state.background
            )
            st.session_state.questions = questions

    answers = []

    for i, question in enumerate(st.session_state.questions):
        answer = st.text_area(
            f"Q{i+1}: {question}",
            height=100,
            key=f"answer_{i}"
        )
        answers.append(answer)

    if st.button("Analyze My Idea 🚀", key="btn_step3"):
        if any(not a.strip() for a in answers):
            st.error("❌ Please answer all questions!")
        else:
            followup_qa = [
                {"question": q, "answer": a}
                for q, a in zip(st.session_state.questions, answers)
            ]
            st.session_state.followup_qa = followup_qa
            st.session_state.step = 4
            st.rerun()


# ─── Step 4: Analysis & Results ──────────────────────────────────────────────

if st.session_state.step == 4:
    st.header("🧠 Step 4: Analysis Results")
    st.divider()

    if st.session_state.analysis is None:
        MAX_RETRIES = 3
        attempt = 0
        success = False
        analysis = None
    
        with st.spinner("⏳ Analyzing your idea... This may take a few seconds..."):
            while attempt < MAX_RETRIES:
                analysis = analyze_idea(
                    st.session_state.idea,
                    st.session_state.founder_name,
                    st.session_state.background,
                    st.session_state.followup_qa
                )
                grade = grade_output(analysis)
    
                if grade["quality_score"] >= 3 and grade.get("feedback", "").strip():
                    success = True
                    break
                
                attempt += 1
    
        if not success:
            st.error("❌ Analysis failed after 3 attempts. Please try again.")
            
            if st.button("🏠 Start Over"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
            
            st.stop()
    
        st.session_state.analysis = analysis

    analysis = st.session_state.analysis

    # ─── Summary ─────────────────────────────────────────────────────────
    st.subheader("📊 Overall Summary")
    st.write(f"**Founder:** {analysis['founder_name']}")
    st.write(f"**Idea:** {analysis['idea_summary']}")
    st.write(f"**Overall Score:** {analysis['overall']['score']}/10")
    st.write(f"**MVP Ready:** {analysis['overall']['is_mvp_ready']}")
    st.write(f"**Investment Ready:** {analysis['overall']['is_investment_ready']}")
    st.write(f"**Incubator Ready:** {analysis['overall']['is_incubator_ready']}")
    st.divider()

    # ─── Scores ──────────────────────────────────────────────────────────
    st.subheader("⭐ Scores (1-10)")
    scores = analysis["scores"]
    for category, data in scores.items():
        st.write(f"**{category.replace('_', ' ').title()}:** {data['score']}/10")
        st.write(f"_{data['reasoning']}_")
    st.divider()

    # ─── Problem & Solution ───────────────────────────────────────────────
    st.subheader("🎯 Problem Statement")
    st.write(analysis["problem_statement"]["description"])
    st.divider()

    st.subheader("💡 Proposed Solution")
    st.write(analysis["proposed_solution"]["what_is_built"])
    st.divider()

    # ─── Download Buttons ─────────────────────────────────────────────────
    st.subheader("📥 Download Reports")

    json_path = save_json(analysis)
    md_path = save_markdown(analysis)

    with open(json_path, "r") as f:
        json_content = f.read()

    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="📦 Download JSON",
            data=json_content,
            file_name="analysis.json",
            mime="application/json"
        )

    with col2:
        st.download_button(
            label="📄 Download Report",
            data=md_content,
            file_name="report.md",
            mime="text/markdown"
        )

    st.divider()

    # ─── Start Over ───────────────────────────────────────────────────────
    if st.button("🔄 Start Over"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()