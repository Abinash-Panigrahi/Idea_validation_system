"""
app.py — Streamlit UI for ThynxAI Idea Lab
Run with: streamlit run app.py
"""

import streamlit as st
from analyzer import (
    validate_input,
    generate_single_question,
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

if "idea_stage" not in st.session_state:
    st.session_state.idea_stage = ""

if "target_market" not in st.session_state:
    st.session_state.target_market = ""

if "team_status" not in st.session_state:
    st.session_state.team_status = ""

if "budget" not in st.session_state:
    st.session_state.budget = ""

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

if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0

if "answers_history" not in st.session_state:
    st.session_state.answers_history = []

if "founder_question_index" not in st.session_state:
    st.session_state.founder_question_index = 0


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
    st.header("👤 Step 2: Founder Information")
    st.divider()

    fq_index = st.session_state.founder_question_index

    # ── Field 0: Name ──
    if fq_index == 0:
        st.write("**What is your name?**")
        founder_name = st.text_input("Your name:", key="input_name")
        if st.button("Next →", key="fq_btn_0"):
            if not founder_name.strip():
                st.error("❌ Please enter your name!")
            else:
                st.session_state.founder_name = founder_name
                st.session_state.founder_question_index = 1
                st.rerun()

    # ── Field 1: Background ──
    elif fq_index == 1:
        st.write("**What is your background?**")
        background = st.selectbox(
            "Select your background:",
            ["Select...", "Technical", "Non-Technical", "Other"],
            key="input_background"
        )
        if st.button("Next →", key="fq_btn_1"):
            if background == "Select...":
                st.error("❌ Please select your background!")
            else:
                st.session_state.background = background
                st.session_state.founder_question_index = 2
                st.rerun()

    # ── Field 2: Idea Stage ──
    elif fq_index == 2:
        st.write("**What stage is your idea at?**")
        idea_stage = st.selectbox(
            "Select your stage:",
            [
                "Select...",
                "Just an idea (thinking stage)",
                "Already researched",
                "Building MVP",
                "Already have users"
            ],
            key="input_stage"
        )
        if st.button("Next →", key="fq_btn_2"):
            if idea_stage == "Select...":
                st.error("❌ Please select your idea stage!")
            else:
                st.session_state.idea_stage = idea_stage
                st.session_state.founder_question_index = 3
                st.rerun()

    # ── Field 3: Target Market ──
    elif fq_index == 3:
        st.write("**What is your target market?**")
        target_market = st.selectbox(
            "Select your target market:",
            [
                "Select...",
                "Local (city level)",
                "India",
                "Global"
            ],
            key="input_market"
        )
        if st.button("Next →", key="fq_btn_3"):
            if target_market == "Select...":
                st.error("❌ Please select your target market!")
            else:
                st.session_state.target_market = target_market
                st.session_state.founder_question_index = 4
                st.rerun()

    # ── Field 4: Team Status ──
    elif fq_index == 4:
        st.write("**What is your team status?**")
        team_status = st.selectbox(
            "Select your team status:",
            [
                "Select...",
                "Solo founder",
                "Have co-founder",
                "Have small team"
            ],
            key="input_team"
        )
        if st.button("Next →", key="fq_btn_4"):
            if team_status == "Select...":
                st.error("❌ Please select your team status!")
            else:
                st.session_state.team_status = team_status
                st.session_state.founder_question_index = 5
                st.rerun()

    # ── Field 5: Budget ──
    elif fq_index == 5:
        st.write("**What is your available budget?**")
        budget = st.selectbox(
            "Select your budget:",
            [
                "Select...",
                "No budget (Bootstrapped)",
                "Under ₹1 lakh",
                "₹1-10 lakh",
                "Above ₹10 lakh"
            ],
            key="input_budget"
        )
        if st.button("Next →", key="fq_btn_5"):
            if budget == "Select...":
                st.error("❌ Please select your budget!")
            else:
                st.session_state.budget = budget
                st.session_state.founder_question_index = 0  # reset for next time
                st.session_state.step = 3
                st.rerun()


# ─── Step 3: Adaptive Questions ──────────────────────────────────────────────

if st.session_state.step == 3:
    st.header("❓ Step 3: Let's Talk About Your Idea!")
    st.divider()

    current_index = st.session_state.current_question_index
    history = st.session_state.answers_history

    # Generate current question if not already generated
    if len(st.session_state.questions) <= current_index:
        with st.spinner(f"⏳ Thinking..."):
            question = generate_single_question(
                st.session_state.idea,
                st.session_state.founder_name,
                st.session_state.background,
                st.session_state.idea_stage,
                st.session_state.target_market,
                st.session_state.team_status,
                st.session_state.budget,
                history
            )
            st.session_state.questions.append(question)

    # Show current question
    current_question = st.session_state.questions[current_index]

    st.divider()
    st.write(f"### 💬 {current_question}")
    st.write("")
    st.write("*You can type your answer below or click 'I Don't Know' if you are unsure!*")

    answer = st.text_area(
        "Your Answer:",
        height=120,
        key=f"answer_{current_index}",
        placeholder="Type your answer here... don't worry, there are no wrong answers!"
    )

    st.write("**OR**")

    # ── Helper Function ──
    def save_and_next(ans):
        st.session_state.answers_history.append({
            "question": current_question,
            "answer": ans
        })
        if current_index < 3:
            st.session_state.current_question_index += 1
        else:
            st.session_state.followup_qa = st.session_state.answers_history
            st.session_state.step = 4
        st.rerun()

    # ── Buttons ──
    col1, col2 = st.columns(2)

    with col1:
        if current_index < 3:
            if st.button("Next →", key=f"btn_q{current_index}", use_container_width=True):
                if not answer.strip():
                    st.error("❌ Please type your answer or click I Don't Know!")
                else:
                    save_and_next(answer)
        else:
            if st.button("Analyze My Idea 🚀", key="btn_analyze", use_container_width=True):
                if not answer.strip():
                    st.error("❌ Please type your answer or click I Don't Know!")
                else:
                    save_and_next(answer)

    with col2:
        if st.button("🤷 I Don't Know", key=f"btn_idk_{current_index}", use_container_width=True):
            save_and_next("I don't know")


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
                    st.session_state.idea_stage,
                    st.session_state.target_market,
                    st.session_state.team_status,
                    st.session_state.budget,
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

            analysis["founder_profile"] = {
            "background": st.session_state.background,
            "idea_stage": st.session_state.idea_stage,
            "target_market": st.session_state.target_market,
            "team_status": st.session_state.team_status,
            "budget": st.session_state.budget
        }
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