import streamlit as st
import matplotlib.pyplot as plt
import matplotlib

st.set_page_config(page_title="MBTI Personality Test", page_icon="🧠", layout="wide")

st.markdown("""
<style>

.block-container {padding-top: 1.2rem;}

.element-container, .stPyplot, .stPlotlyChart {
    background: transparent !important;
    padding: 0 !important;
}

div[data-testid="stDecoration"] {display: none !important;}
div[data-testid="stPlot"] {background: transparent !important;}

.intro-box {
    background: linear-gradient(135deg, #8b5cff 0%, #6fd6ff 100%);
    padding: 70px;
    border-radius: 25px;
    text-align: center;
    color: white;
    margin-top: 40px;
}

.intro-title {
    font-size: 55px;
    font-weight: 900;
}

.intro-sub {
    font-size: 22px;
    margin-top: 10px;
}

button[kind="primary"] {
    background: #7b4bff !important;
    color: white !important;
    border-radius: 12px !important;
    font-size: 18px !important;
    padding: 12px 20px !important;
}
button[kind="primary"]:hover {
    background: #9d7bff !important;
}

html {scroll-behavior: smooth;}

</style>
""", unsafe_allow_html=True)

if "stage" not in st.session_state:
    st.session_state.stage = "intro"

if "answers" not in st.session_state:
    st.session_state.answers = {}

questions = [
    {"key": "q1", "dimension": "EI", "question": "At social events, you usually…",
     "options": [("Start conversations with many people.", "E"),
                 ("Talk with 1–2 close friends.", "I"),
                 ("Stay quiet & observe.", "I")]},

    {"key": "q2", "dimension": "EI", "question": "What energizes you most?",
     "options": [("People around me.", "E"),
                 ("Being alone.", "I"),
                 ("Mostly alone time.", "I")]},

    {"key": "q3", "dimension": "SN", "question": "You trust information that is…",
     "options": [("Practical & real.", "S"),
                 ("Abstract & creative.", "N"),
                 ("Patterns & ideas.", "N")]},

    {"key": "q4", "dimension": "SN", "question": "When learning something new…",
     "options": [("I need clear examples.", "S"),
                 ("I like exploring concepts.", "N"),
                 ("I enjoy imagining possibilities.", "N")]},

    {"key": "q5", "dimension": "TF", "question": "You usually decide based on…",
     "options": [("Logic & reasoning.", "T"),
                 ("Feelings & harmony.", "F"),
                 ("Others' emotions.", "F")]},

    {"key": "q6", "dimension": "TF", "question": "In arguments, you…",
     "options": [("Stick to facts.", "T"),
                 ("Try to keep peace.", "F"),
                 ("Consider feelings.", "F")]},

    {"key": "q7", "dimension": "JP", "question": "Your work style is…",
     "options": [("Organized & planned.", "J"),
                 ("Flexible.", "P"),
                 ("Spontaneous.", "P")]},

    {"key": "q8", "dimension": "JP", "question": "Last-minute changes are…",
     "options": [("Annoying.", "J"),
                 ("Depends on mood.", "P"),
                 ("Exciting.", "P")]},

    {"key": "q9", "dimension": "EI", "question": "How do you recharge?",
     "options": [("Talking to others.", "E"),
                 ("Quiet alone time.", "I"),
                 ("Being alone outdoors.", "I")]},

    {"key": "q10", "dimension": "JP", "question": "Your workspace is usually…",
     "options": [("Neat & organized.", "J"),
                 ("A little messy.", "P"),
                 ("Unpredictable.", "P")]}
]

desc = {
    "E": "Extraversion – Social & energetic.",
    "I": "Introversion – Reflective & independent.",
    "S": "Sensing – Realistic & detail-focused.",
    "N": "Intuition – Creative & imaginative.",
    "T": "Thinking – Logical & reason-based.",
    "F": "Feeling – Empathetic & values emotions.",
    "J": "Judging – Structured & organized.",
    "P": "Perceiving – Flexible & spontaneous."
}

# INTRO
if st.session_state.stage == "intro":

    st.markdown("""
        <div class='intro-box'>
            <div class='intro-title'>🧠 MBTI Personality Test</div>
            <div class='intro-sub'>Take this 10-question test and discover your personality type instantly.</div>
        </div>
    """, unsafe_allow_html=True)

    st.write("### ✨ What You Will Get")
    st.write("- Your 4-letter MBTI Type")
    st.write("- Detailed Personality Traits")
    st.write("- Visual Trait Graph")
    st.write("- Clean and Modern UI")

    if st.button("👉 Start the Test"):
        st.session_state.stage = "quiz"
        st.rerun()

# QUIZ
elif st.session_state.stage == "quiz":

    st.markdown("<h1>📝 MBTI Quiz</h1>", unsafe_allow_html=True)

    for q in questions:
        st.markdown(f"### {q['question']}")
        answer = st.radio("", [txt for txt, _ in q["options"]], key=q["key"], index=None)
        st.session_state.answers[q["key"]] = answer

    if st.button("Submit Test"):
        if None in st.session_state.answers.values():
            st.warning("⚠️ Please answer all questions!")
        else:
            st.session_state.stage = "result"
            st.rerun()

# RESULT
elif st.session_state.stage == "result":

    score = {"E":0,"I":0,"S":0,"N":0,"T":0,"F":0,"J":0,"P":0}

    for q in questions:
        selected = st.session_state.answers[q["key"]]
        for txt, letter in q["options"]:
            if txt == selected:
                score[letter] += 1

    EI = "E" if score["E"] >= score["I"] else "I"
    SN = "S" if score["S"] >= score["N"] else "N"
    TF = "T" if score["T"] >= score["F"] else "F"
    JP = "J" if score["J"] >= score["P"] else "P"
    mbti = EI + SN + TF + JP

    st.markdown(f"<h1>🎉 Your MBTI Type: <b>{mbti}</b></h1>", unsafe_allow_html=True)

    st.write("### 🔍 Personality Breakdown")
    for letter in mbti:
        st.write(f"**{letter} – {desc[letter]}**")

    st.write("---")
    st.write("### 📊 Trait Graph")

    labels = ["E","I","S","N","T","F","J","P"]
    values = [score[l] for l in labels]

    matplotlib.use("Agg")
    fig, ax = plt.subplots(figsize=(4.5, 1.8), dpi=165)

    fig.patch.set_facecolor("none")
    ax.set_facecolor("none")

    ax.bar(labels, values, color="#b28bff", edgecolor="none", width=0.55)
    ax.tick_params(colors="white", labelsize=9)
    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.margins(x=0.05, y=0.15)
    plt.tight_layout()

    cols = st.columns([1, 1.4, 1])
    with cols[1]:
        st.pyplot(fig, clear_figure=True)

    st.write("---")

    if st.button("🔁 Take Test Again"):
        st.session_state.stage = "intro"
        st.session_state.answers = {}
        st.rerun()

    # Force scroll to very top when result page is shown
    st.markdown(
        """
        <script>
        const sec = window.parent.document.querySelector('section.main');
        if (sec) { sec.scrollTo({top: 0, left: 0, behavior: 'smooth'}); }
        </script>
        """,
        unsafe_allow_html=True,
    )
