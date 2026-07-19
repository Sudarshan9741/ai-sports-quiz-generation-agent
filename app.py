import streamlit as st
from src.generator import generate_quiz

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Sports Quiz Generator",
    page_icon="🏆",
    layout="wide",
)

# --------------------------------------------------
# COLORS
# --------------------------------------------------

BACKGROUND = "#0E1628"
CARD = "#182437"
PRIMARY = "#F28C28"
PRIMARY_HOVER = "#D97706"
TEXT = "#F8FAFC"
SECONDARY = "#B6C2D1"
BORDER = "#273449"

# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown(
    f"""
<style>

.stApp {{
    background:{BACKGROUND};
}}

.block-container {{
    max-width:1200px;
    padding-top:2rem;
}}

section[data-testid="stSidebar"] {{
    background:{CARD};
}}

.hero {{
    background:{CARD};
    border:1px solid {BORDER};
    border-radius:18px;
    padding:30px;
    margin-bottom:30px;
}}

.hero h1 {{
    color:{TEXT};
    font-size:42px;
    margin-bottom:10px;
}}

.hero p {{
    color:{SECONDARY};
    font-size:18px;
}}

.settings {{
    background:{CARD};
    border:1px solid {BORDER};
    border-radius:18px;
    padding:25px;
    margin-top:20px;
    margin-bottom:20px;
}}

.stButton>button {{
    width:100%;
    background:{PRIMARY};
    color:white;
    border:none;
    border-radius:10px;
    padding:14px;
    font-size:18px;
    font-weight:bold;
}}

.stButton>button:hover {{
    background:{PRIMARY_HOVER};
}}

div[data-baseweb="select"]>div {{
    background:{CARD};
}}

.question-card {{
    background:{CARD};
    border:1px solid {BORDER};
    border-radius:16px;
    padding:25px;
    margin-bottom:25px;
}}

.answer {{
    background:#163B2F;
    padding:12px;
    border-radius:10px;
    margin-top:15px;
}}

.explanation {{
    background:#1E3A5F;
    padding:12px;
    border-radius:10px;
    margin-top:12px;
}}

</style>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.title("🏆 AI Quiz")

# --------------------------------------------------
# HERO
# --------------------------------------------------

st.markdown(
    """
<div class="hero">

<h1>🏆 AI Sports Quiz Generator</h1>

<p>
Generate sports quizzes instantly.
Choose your favourite sport,
select a difficulty level,
and let AI create a complete quiz.
</p>

</div>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

st.subheader(" Quiz Type")
st.write("")

col1, col2 = st.columns(2, gap="large")

with col1:
    sport = st.selectbox(
        "🏏 Sport",
        [
            "Cricket",
            "Football",
            "Basketball",
            "Tennis",
            "Olympics",
        ],
    )

with col2:
    difficulty = st.selectbox(
        "🎯 Difficulty",
        [
            "Easy",
            "Medium",
            "Hard",
        ],
    )

left, center, right = st.columns([2, 1, 2])

with center:
    generate = st.button("🚀 Generate Quiz")

quiz = None

if generate:

    with st.spinner("Generating quiz..."):

        quiz = generate_quiz(
            sport=sport,
            difficulty=difficulty,
        )
# --------------------------------------------------
# QUIZ DISPLAY
# --------------------------------------------------

if quiz:

    st.divider()

    st.subheader("📋 Generated Quiz")

    import re

    quiz = quiz.replace("\r", "")

    questions = re.split(r"Question\s+\d+", quiz)
    questions = [q.strip() for q in questions if q.strip()]

    if not questions:
        st.error("Unable to read quiz.")
        st.stop()

    for index, block in enumerate(questions, start=1):

        st.markdown(
            f"""
<div class="question-card">
<h3>🏆 Question {index}</h3>
</div>
""",
            unsafe_allow_html=True,
        )

        lines = [line.strip() for line in block.split("\n") if line.strip()]

        question = ""
        options = []
        answer = ""
        explanation = ""

        mode = None

        for line in lines:

            # ------------------------------
            # Correct Answer
            # ------------------------------
            if line.lower().startswith("correct answer"):
                mode = "answer"

                if ":" in line:
                    answer = line.split(":", 1)[1].strip()

            # ------------------------------
            # Explanation
            # ------------------------------
            elif line.lower().startswith("explanation"):
                mode = "explanation"

                if ":" in line:
                    explanation = line.split(":", 1)[1].strip()

            # ------------------------------
            # Options OR Answer
            # ------------------------------
            elif line.startswith(("A)", "B)", "C)", "D)")):

                if mode == "answer":
                    answer = line
                else:
                    options.append(line)

            # ------------------------------
            # Question / Explanation
            # ------------------------------
            else:

                if not question:
                    question = line

                elif mode == "answer":
                    answer += " " + line

                elif mode == "explanation":
                    explanation += " " + line

        # Remove A), B), C), D) from answer
        answer = re.sub(r"^[A-D]\)\s*", "", answer)

        st.markdown(f"### {question}")

        st.write("")

        # ------------------------------
        # Options
        # ------------------------------
        for option in options:

            st.markdown(
                f"""
<div style="
background:#111827;
padding:12px;
border-radius:10px;
margin-bottom:10px;
border:1px solid #273449;
">
{option}
</div>
""",
                unsafe_allow_html=True,
            )

        st.write("")

        # ------------------------------
        # Correct Answer
        # ------------------------------
        st.markdown(
            f"""
<div class="answer">

<h4 style="margin:0;">✅ Correct Answer</h4>

<p style="margin-top:12px;font-size:18px;">
<b>{answer}</b>
</p>

</div>
""",
            unsafe_allow_html=True,
        )

        # ------------------------------
        # Explanation
        # ------------------------------
        st.markdown(
            f"""
<div class="explanation">

<h4 style="margin:0;">💡 Explanation</h4>

<p style="margin-top:12px;font-size:17px;">
{explanation}
</p>

</div>
""",
            unsafe_allow_html=True,
        )

        st.write("")
        st.write("")

elif generate:

    st.error("❌ Unable to generate quiz.")