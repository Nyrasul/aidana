import streamlit as st
import json
import random
import time

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="⚕️ MedQuiz",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── GLOBAL CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
}

/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #0f1117 0%, #1a1f2e 50%, #0d1520 100%);
    min-height: 100vh;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #131929 0%, #0e1621 100%);
    border-right: 1px solid rgba(99,179,237,0.15);
}
[data-testid="stSidebar"] * { color: #c8d6e8 !important; }
[data-testid="stSidebar"] .stSlider label { color: #7eb3d8 !important; }

/* ── Sidebar header ── */
.sidebar-brand {
    text-align: center;
    padding: 1.5rem 0 1rem;
    border-bottom: 1px solid rgba(99,179,237,0.2);
    margin-bottom: 1.5rem;
}
.sidebar-brand h1 {
    font-size: 1.6rem;
    font-weight: 700;
    background: linear-gradient(135deg, #63b3ed, #90cdf4, #4299e1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    letter-spacing: -0.5px;
}
.sidebar-brand p {
    color: #5a7a9a !important;
    font-size: 0.75rem;
    margin: 0.2rem 0 0;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* ── Stat chips in sidebar ── */
.stat-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(99,179,237,0.1);
    border: 1px solid rgba(99,179,237,0.2);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.75rem;
    color: #90cdf4;
    margin: 2px;
}

/* ── Main card ── */
.quiz-card {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(99,179,237,0.15);
    border-radius: 20px;
    padding: 2.2rem 2.4rem;
    margin-bottom: 1.4rem;
    box-shadow: 0 8px 40px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
    position: relative;
    overflow: hidden;
}
.quiz-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #4299e1 40%, #63b3ed 60%, transparent);
}

/* ── Progress bar wrapper ── */
.progress-wrapper {
    margin: 0.8rem 0 1.6rem;
}
.progress-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.78rem;
    color: #5a7a9a;
    margin-bottom: 6px;
    font-family: 'JetBrains Mono', monospace;
}
.progress-track {
    height: 6px;
    background: rgba(255,255,255,0.08);
    border-radius: 3px;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    border-radius: 3px;
    background: linear-gradient(90deg, #2d6a9f, #4299e1, #63b3ed);
    transition: width 0.5s ease;
    box-shadow: 0 0 8px rgba(66,153,225,0.5);
}

/* ── Question text ── */
.question-num {
    font-size: 0.72rem;
    color: #4a7fa5;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.7rem;
}
.question-text {
    font-size: 1.08rem;
    font-weight: 500;
    color: #dde8f5;
    line-height: 1.7;
    margin-bottom: 1.6rem;
}

/* ── Answer option buttons ── */
div[data-testid="stButton"] > button {
    width: 100%;
    text-align: left;
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(99,179,237,0.15) !important;
    border-radius: 12px !important;
    padding: 0.85rem 1.2rem !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 0.92rem !important;
    color: #b8cfe0 !important;
    transition: all 0.22s ease !important;
    margin-bottom: 0 !important;
    cursor: pointer !important;
}
div[data-testid="stButton"] > button:hover {
    background: rgba(66,153,225,0.12) !important;
    border-color: rgba(99,179,237,0.45) !important;
    color: #e8f4ff !important;
    transform: translateX(4px);
    box-shadow: 0 4px 20px rgba(66,153,225,0.15) !important;
}

/* ── Correct / Incorrect feedback states ── */
.answer-correct {
    background: rgba(72,187,120,0.12) !important;
    border: 1px solid rgba(72,187,120,0.5) !important;
    color: #9ae6b4 !important;
    border-radius: 12px;
    padding: 0.85rem 1.2rem;
    font-size: 0.92rem;
    margin-bottom: 6px;
    transition: all 0.3s;
}
.answer-incorrect {
    background: rgba(245,101,101,0.1) !important;
    border: 1px solid rgba(245,101,101,0.4) !important;
    color: #fc8181 !important;
    border-radius: 12px;
    padding: 0.85rem 1.2rem;
    font-size: 0.92rem;
    margin-bottom: 6px;
}
.answer-neutral {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(99,179,237,0.12);
    border-radius: 12px;
    padding: 0.85rem 1.2rem;
    font-size: 0.92rem;
    color: #7896b0;
    margin-bottom: 6px;
}
.answer-was-correct {
    background: rgba(72,187,120,0.08);
    border: 1px solid rgba(72,187,120,0.35);
    border-radius: 12px;
    padding: 0.85rem 1.2rem;
    font-size: 0.92rem;
    color: #68d391;
    margin-bottom: 6px;
}

/* ── Explanation / Feedback box ── */
.feedback-box {
    border-radius: 14px;
    padding: 1rem 1.3rem;
    margin-top: 1rem;
    font-size: 0.88rem;
    line-height: 1.6;
    display: flex;
    align-items: flex-start;
    gap: 10px;
}
.feedback-correct {
    background: rgba(72,187,120,0.1);
    border: 1px solid rgba(72,187,120,0.3);
    color: #9ae6b4;
}
.feedback-incorrect {
    background: rgba(245,101,101,0.08);
    border: 1px solid rgba(245,101,101,0.3);
    color: #fc8181;
}
.feedback-icon { font-size: 1.3rem; margin-top: 1px; }
.feedback-text strong { display: block; margin-bottom: 3px; font-size: 0.95rem; }

/* ── Nav buttons ── */
.nav-btn {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(99,179,237,0.2) !important;
    border-radius: 10px !important;
    color: #90cdf4 !important;
    padding: 0.6rem 1.4rem !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}
.nav-btn:hover {
    background: rgba(66,153,225,0.15) !important;
    border-color: rgba(99,179,237,0.5) !important;
}

/* ── Primary CTA buttons ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #2b6cb0, #4299e1) !important;
    border: none !important;
    border-radius: 12px !important;
    color: white !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 15px rgba(66,153,225,0.4) !important;
}

/* ── Score card ── */
.score-card {
    text-align: center;
    padding: 2.5rem;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(99,179,237,0.15);
    border-radius: 20px;
    margin: 1rem 0;
}
.score-big {
    font-size: 4rem;
    font-weight: 700;
    background: linear-gradient(135deg, #63b3ed, #90cdf4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
    margin: 0.5rem 0;
}
.score-label {
    color: #5a7a9a;
    font-size: 0.85rem;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.score-grade {
    font-size: 1.1rem;
    font-weight: 600;
    margin-top: 0.8rem;
}

/* ── Mini stats row ── */
.mini-stats {
    display: flex;
    gap: 1rem;
    margin: 1.2rem 0;
    flex-wrap: wrap;
}
.mini-stat {
    flex: 1;
    min-width: 100px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(99,179,237,0.12);
    border-radius: 12px;
    padding: 0.9rem;
    text-align: center;
}
.mini-stat .num {
    font-size: 1.6rem;
    font-weight: 700;
    color: #90cdf4;
    font-family: 'JetBrains Mono', monospace;
}
.mini-stat .lbl {
    font-size: 0.72rem;
    color: #5a7a9a;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 2px;
}

/* ── Welcome screen ── */
.welcome-hero {
    text-align: center;
    padding: 3rem 2rem;
}
.welcome-icon { font-size: 5rem; margin-bottom: 1rem; }
.welcome-title {
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(135deg, #90cdf4, #63b3ed, #4299e1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.8rem;
}
.welcome-sub {
    color: #5a7a9a;
    font-size: 1rem;
    max-width: 480px;
    margin: 0 auto 2rem;
    line-height: 1.7;
}

/* ── Reviewed questions panel ── */
.reviewed-dot {
    display: inline-block;
    width: 10px; height: 10px;
    border-radius: 50%;
    margin: 2px;
    cursor: pointer;
}

/* ── Slider ── */
.stSlider > div > div { background: rgba(99,179,237,0.25) !important; }
.stSlider [data-testid="stThumbValue"] { color: #90cdf4 !important; }

/* ── Multiselect ── */
.stMultiSelect [data-baseweb="select"] {
    background: rgba(255,255,255,0.05) !important;
    border-color: rgba(99,179,237,0.2) !important;
}

/* ── Divider ── */
hr { border-color: rgba(99,179,237,0.1) !important; margin: 1.2rem 0 !important; }

/* ── Bookmarks bar ── */
.bookmark-bar {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    padding: 0.8rem;
    background: rgba(255,200,80,0.05);
    border: 1px solid rgba(255,200,80,0.15);
    border-radius: 12px;
    margin-bottom: 1rem;
}
.bm-tag {
    background: rgba(255,200,80,0.12);
    border: 1px solid rgba(255,200,80,0.25);
    border-radius: 8px;
    padding: 2px 10px;
    font-size: 0.78rem;
    color: #fbd38d;
}

/* ── Timer bar ── */
.timer-bar {
    height: 4px;
    background: rgba(255,255,255,0.08);
    border-radius: 2px;
    margin-bottom: 1rem;
    overflow: hidden;
}

/* ── Toast notification ── */
.toast {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
    padding: 0.7rem 1.2rem;
    border-radius: 10px;
    font-size: 0.88rem;
    font-weight: 500;
    animation: slideIn 0.3s ease;
}
@keyframes slideIn {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; max-width: 860px !important; }

/* Radio buttons override */
.stRadio > div { gap: 0 !important; }
.stRadio [data-testid="stWidgetLabel"] { color: #7896b0 !important; font-size: 0.82rem !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.03); }
::-webkit-scrollbar-thumb { background: rgba(99,179,237,0.3); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ─── DATA LOADING ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    with open("questions.json", "r", encoding="utf-8") as f:
        return json.load(f)

questions = load_data()


# ─── SESSION STATE DEFAULTS ───────────────────────────────────────────────────
def init_state():
    defaults = {
        'quiz_data': None,
        'current_q': 0,
        'user_answers': {},
        'revealed': {},          # {q_idx: True} when answer checked
        'show_final': False,
        'failed_questions': [],
        'bookmarks': set(),
        'shuffle_options': True,
        'shuffled_options': {},  # store shuffled options per question
        'session_start': None,
        'correct_streak': 0,
        'high_streak': 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <h1>🧬 MedQuiz</h1>
        <p>Pharmacognosy · KZ</p>
    </div>
    """, unsafe_allow_html=True)

    sources = sorted(set(q.get('source', 'Unknown') for q in questions))
    selected_sources = st.multiselect("📂 Question Bank", sources, default=sources)
    filtered_questions = [q for q in questions if q.get('source', 'Unknown') in selected_sources]
    total_available = len(filtered_questions)

    st.markdown(f"<div style='color:#4a7fa5;font-size:0.78rem;margin:0.3rem 0 0.8rem;font-family:JetBrains Mono,monospace;'>{total_available} questions available</div>", unsafe_allow_html=True)

    if total_available > 0:
        num_q = st.slider("📝 Number of Questions", 1, total_available, min(20, total_available))

        st.markdown("---")
        st.markdown("**⚙️ Options**")

        shuffle_q = st.checkbox("🔀 Shuffle question order", value=True)
        shuffle_opts = st.checkbox("🔀 Shuffle answer options", value=True)
        show_streak = st.checkbox("🔥 Show streak counter", value=True)

        st.markdown("---")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🚀 Start Test", use_container_width=True):
                pool = filtered_questions.copy()
                if shuffle_q:
                    random.shuffle(pool)
                selected = pool[:num_q]

                # Pre-shuffle options if enabled
                shuffled_opts = {}
                for i, q in enumerate(selected):
                    if shuffle_opts:
                        opts = q['options'].copy()
                        random.shuffle(opts)
                        shuffled_opts[i] = opts
                    else:
                        shuffled_opts[i] = q['options'].copy()

                st.session_state.quiz_data = selected
                st.session_state.current_q = 0
                st.session_state.user_answers = {}
                st.session_state.revealed = {}
                st.session_state.show_final = False
                st.session_state.failed_questions = []
                st.session_state.bookmarks = set()
                st.session_state.shuffle_options = shuffle_opts
                st.session_state.shuffled_options = shuffled_opts
                st.session_state.session_start = time.time()
                st.session_state.correct_streak = 0
                st.session_state.high_streak = 0
                st.rerun()

        with col_b:
            if st.button("🔖 Retry\nFailed", use_container_width=True):
                if st.session_state.failed_questions:
                    pool = st.session_state.failed_questions.copy()
                    random.shuffle(pool)
                    shuffled_opts = {}
                    for i, q in enumerate(pool):
                        opts = q['options'].copy()
                        random.shuffle(opts)
                        shuffled_opts[i] = opts

                    st.session_state.quiz_data = pool
                    st.session_state.current_q = 0
                    st.session_state.user_answers = {}
                    st.session_state.revealed = {}
                    st.session_state.show_final = False
                    st.session_state.shuffled_options = shuffled_opts
                    st.session_state.session_start = time.time()
                    st.session_state.correct_streak = 0
                    st.rerun()

        # Bookmark quick-jump
        if st.session_state.quiz_data and st.session_state.bookmarks:
            st.markdown("---")
            st.markdown("**🔖 Bookmarked**")
            for bm_i in sorted(st.session_state.bookmarks):
                if bm_i < len(st.session_state.quiz_data):
                    if st.button(f"Q{bm_i+1}", key=f"bm_jump_{bm_i}", use_container_width=True):
                        st.session_state.current_q = bm_i
                        st.session_state.show_final = False
                        st.rerun()

        # Live score in sidebar
        if st.session_state.quiz_data and st.session_state.user_answers:
            answered = len(st.session_state.revealed)
            correct = sum(
                1 for i in st.session_state.revealed
                if st.session_state.user_answers.get(i) == st.session_state.quiz_data[i]['correct_answer']
            )
            st.markdown("---")
            st.markdown(f"""
            <div style='text-align:center;padding:0.8rem 0;'>
                <div style='font-size:1.8rem;font-weight:700;color:#63b3ed;font-family:JetBrains Mono,monospace;'>{correct}/{answered}</div>
                <div style='font-size:0.72rem;color:#4a7fa5;text-transform:uppercase;letter-spacing:1px;'>Live Score</div>
            </div>
            """, unsafe_allow_html=True)

            if show_streak and st.session_state.correct_streak > 1:
                st.markdown(f"<div style='text-align:center;color:#f6ad55;font-weight:600;'>🔥 {st.session_state.correct_streak} streak!</div>", unsafe_allow_html=True)
    else:
        st.warning("No questions match your selection.")


# ─── MAIN CONTENT ─────────────────────────────────────────────────────────────
if st.session_state.quiz_data is None:
    # ── Welcome Screen ──
    st.markdown("""
    <div class="quiz-card">
        <div class="welcome-hero">
            <div class="welcome-icon">🧬</div>
            <div class="welcome-title">MedQuiz</div>
            <div class="welcome-sub">
                Your smart study companion for Pharmacognosy.<br>
                Configure your session in the sidebar and hit <strong style='color:#63b3ed;'>Start Test</strong>.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="quiz-card" style="text-align:center;padding:1.4rem;">
            <div style="font-size:2rem;margin-bottom:0.5rem;">🔀</div>
            <div style="font-weight:600;color:#90cdf4;margin-bottom:0.4rem;">Shuffle Mode</div>
            <div style="font-size:0.82rem;color:#5a7a9a;">Randomize questions and options for spaced practice</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="quiz-card" style="text-align:center;padding:1.4rem;">
            <div style="font-size:2rem;margin-bottom:0.5rem;">🔥</div>
            <div style="font-weight:600;color:#90cdf4;margin-bottom:0.4rem;">Streak Tracking</div>
            <div style="font-size:0.82rem;color:#5a7a9a;">Stay motivated with live streak and score counters</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="quiz-card" style="text-align:center;padding:1.4rem;">
            <div style="font-size:2rem;margin-bottom:0.5rem;">📌</div>
            <div style="font-weight:600;color:#90cdf4;margin-bottom:0.4rem;">Bookmarks</div>
            <div style="font-size:0.82rem;color:#5a7a9a;">Flag tricky questions and revisit them instantly</div>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='text-align:center;margin-top:1rem;'>
        <span class='stat-chip'>📚 {len(questions)} Total Questions</span>
        <span class='stat-chip'>📁 {len(set(q.get('source','?') for q in questions))} Source Files</span>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.show_final:
    # ── Final Results Screen ──
    quiz = st.session_state.quiz_data
    total = len(quiz)
    correct_count = sum(
        1 for i, q in enumerate(quiz)
        if st.session_state.user_answers.get(i) == q['correct_answer']
    )
    wrong_count = total - correct_count
    pct = (correct_count / total * 100) if total else 0

    if pct >= 90:
        grade_emoji, grade_text, grade_color = "🏆", "Outstanding!", "#f6e05e"
    elif pct >= 75:
        grade_emoji, grade_text, grade_color = "🎉", "Great job!", "#68d391"
    elif pct >= 60:
        grade_emoji, grade_text, grade_color = "👍", "Good effort!", "#63b3ed"
    elif pct >= 40:
        grade_emoji, grade_text, grade_color = "📚", "Keep studying!", "#f6ad55"
    else:
        grade_emoji, grade_text, grade_color = "💪", "Don't give up!", "#fc8181"

    elapsed = ""
    if st.session_state.session_start:
        secs = int(time.time() - st.session_state.session_start)
        elapsed = f"{secs // 60}m {secs % 60}s"

    st.markdown(f"""
    <div class="quiz-card">
        <div class="score-card">
            <div style="font-size:2.5rem;">{grade_emoji}</div>
            <div class="score-label">Your Score</div>
            <div class="score-big">{pct:.0f}%</div>
            <div class="score-grade" style="color:{grade_color};">{grade_text}</div>
        </div>
        <div class="mini-stats">
            <div class="mini-stat">
                <div class="num" style="color:#68d391;">{correct_count}</div>
                <div class="lbl">Correct</div>
            </div>
            <div class="mini-stat">
                <div class="num" style="color:#fc8181;">{wrong_count}</div>
                <div class="lbl">Wrong</div>
            </div>
            <div class="mini-stat">
                <div class="num">{total}</div>
                <div class="lbl">Total</div>
            </div>
            <div class="mini-stat">
                <div class="num" style="color:#f6ad55;">{st.session_state.high_streak}</div>
                <div class="lbl">Best Streak</div>
            </div>
            {'<div class="mini-stat"><div class="num" style="color:#b794f4;">'+elapsed+'</div><div class="lbl">Time</div></div>' if elapsed else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Action buttons
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔁 New Test", use_container_width=True):
            st.session_state.quiz_data = None
            st.session_state.show_final = False
            st.rerun()
    with c2:
        if wrong_count > 0:
            if st.button(f"📌 Retry {wrong_count} Failed", use_container_width=True):
                failed = [q for i, q in enumerate(quiz)
                          if st.session_state.user_answers.get(i) != q['correct_answer']]
                random.shuffle(failed)
                shuffled_opts = {}
                for i, q in enumerate(failed):
                    opts = q['options'].copy()
                    random.shuffle(opts)
                    shuffled_opts[i] = opts
                st.session_state.quiz_data = failed
                st.session_state.failed_questions = []
                st.session_state.current_q = 0
                st.session_state.user_answers = {}
                st.session_state.revealed = {}
                st.session_state.show_final = False
                st.session_state.shuffled_options = shuffled_opts
                st.session_state.session_start = time.time()
                st.session_state.correct_streak = 0
                st.rerun()
    with c3:
        if st.button("📖 Review All", use_container_width=True):
            st.session_state.show_final = False
            st.session_state.current_q = 0
            st.rerun()

    # Results breakdown
    if total > 0:
        st.markdown("<div style='color:#5a7a9a;font-size:0.82rem;margin:1.2rem 0 0.5rem;text-transform:uppercase;letter-spacing:1px;'>Results breakdown</div>", unsafe_allow_html=True)
        cols = st.columns(min(10, total))
        for i in range(total):
            is_right = st.session_state.user_answers.get(i) == quiz[i]['correct_answer']
            color = "#68d391" if is_right else "#fc8181"
            icon = "✓" if is_right else "✗"
            with cols[i % len(cols)]:
                if st.button(f"{icon}", key=f"res_jump_{i}", help=f"Q{i+1}"):
                    st.session_state.show_final = False
                    st.session_state.current_q = i
                    st.rerun()

else:
    # ── Active Quiz Screen ──
    quiz = st.session_state.quiz_data
    ci = st.session_state.current_q
    q_data = quiz[ci]
    total_q = len(quiz)
    options = st.session_state.shuffled_options.get(ci, q_data['options'])

    # Progress
    pct_done = (ci / total_q) * 100
    answered_so_far = len(st.session_state.revealed)
    correct_so_far = sum(
        1 for idx in st.session_state.revealed
        if st.session_state.user_answers.get(idx) == quiz[idx]['correct_answer']
    )

    # ── Top bar: progress + bookmark ──
    top_left, top_right = st.columns([5, 1])
    with top_left:
        st.markdown(f"""
        <div class="progress-wrapper">
            <div class="progress-label">
                <span>Question {ci+1} of {total_q}</span>
                <span>{answered_so_far} answered · {correct_so_far} correct</span>
            </div>
            <div class="progress-track">
                <div class="progress-fill" style="width:{pct_done}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with top_right:
        bm_label = "🔖 Saved" if ci in st.session_state.bookmarks else "🔖 Save"
        if st.button(bm_label, key="bookmark_btn"):
            if ci in st.session_state.bookmarks:
                st.session_state.bookmarks.discard(ci)
            else:
                st.session_state.bookmarks.add(ci)
            st.rerun()

    # ── Question card ──
    is_revealed = st.session_state.revealed.get(ci, False)
    user_choice = st.session_state.user_answers.get(ci)
    correct_ans = q_data['correct_answer']

    st.markdown(f"""
    <div class="quiz-card">
        <div class="question-num">Q {ci+1:03d} / {total_q:03d}</div>
        <div class="question-text">{q_data['question']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Images (if any)
    if q_data.get("images"):
        for img in q_data["images"]:
            st.image(img, use_container_width=True)

    # ── Answer options ──
    if not is_revealed:
        # Interactive selection
        current_choice = st.session_state.user_answers.get(ci, options[0])
        chosen = st.radio(
            "Select your answer:",
            options,
            index=options.index(current_choice) if current_choice in options else 0,
            key=f"radio_{ci}",
            label_visibility="collapsed"
        )
        st.session_state.user_answers[ci] = chosen

        # Check answer button
        st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
        if st.button("✅ Check Answer", key="check_btn", use_container_width=True):
            st.session_state.revealed[ci] = True
            if chosen == correct_ans:
                st.session_state.correct_streak += 1
                if st.session_state.correct_streak > st.session_state.high_streak:
                    st.session_state.high_streak = st.session_state.correct_streak
            else:
                st.session_state.correct_streak = 0
            st.rerun()
    else:
        # Show revealed answers with color coding
        for opt in options:
            if opt == correct_ans and opt == user_choice:
                st.markdown(f'<div class="answer-correct">✅ {opt}</div>', unsafe_allow_html=True)
            elif opt == user_choice and opt != correct_ans:
                st.markdown(f'<div class="answer-incorrect">❌ {opt}</div>', unsafe_allow_html=True)
            elif opt == correct_ans:
                st.markdown(f'<div class="answer-was-correct">☑ {opt} ← correct</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="answer-neutral">{opt}</div>', unsafe_allow_html=True)

        # Feedback box
        is_correct = user_choice == correct_ans
        streak_msg = ""
        if is_correct and st.session_state.correct_streak > 2:
            streak_msg = f" &nbsp;·&nbsp; 🔥 {st.session_state.correct_streak} in a row!"

        if is_correct:
            st.markdown(f"""
            <div class="feedback-box feedback-correct">
                <div class="feedback-icon">✅</div>
                <div class="feedback-text">
                    <strong>Correct!{streak_msg}</strong>
                    The right answer is: <em>{correct_ans}</em>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="feedback-box feedback-incorrect">
                <div class="feedback-icon">❌</div>
                <div class="feedback-text">
                    <strong>Incorrect.</strong>
                    The correct answer is: <em>{correct_ans}</em>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Navigation ──
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    nav1, nav2, nav3, nav4 = st.columns([1, 1, 2, 1])

    with nav1:
        if st.button("⬅ Prev", disabled=(ci == 0), use_container_width=True):
            st.session_state.current_q -= 1
            st.rerun()

    with nav2:
        if st.button("Next ➡", disabled=(ci == total_q - 1), use_container_width=True):
            st.session_state.current_q += 1
            st.rerun()

    with nav3:
        # Quick jump selector
        jump_to = st.selectbox(
            "Jump to question",
            range(1, total_q + 1),
            index=ci,
            key="jump_sel",
            label_visibility="collapsed",
            format_func=lambda x: f"Q{x}" + (" ✓" if (x-1) in st.session_state.revealed and st.session_state.user_answers.get(x-1) == quiz[x-1]['correct_answer']
                                              else " ✗" if (x-1) in st.session_state.revealed else "")
        )
        if jump_to - 1 != ci:
            st.session_state.current_q = jump_to - 1
            st.rerun()

    with nav4:
        if st.button("🏁 Finish", type="primary", use_container_width=True):
            st.session_state.failed_questions = [
                q for i, q in enumerate(quiz)
                if st.session_state.user_answers.get(i) != q['correct_answer']
            ]
            st.session_state.show_final = True
            st.rerun()

    # ── Question map at bottom ──
    with st.expander("🗺 Question Map", expanded=False):
        map_cols = st.columns(min(10, total_q))
        for i in range(total_q):
            is_answered = i in st.session_state.revealed
            is_right = is_answered and st.session_state.user_answers.get(i) == quiz[i]['correct_answer']
            is_bm = i in st.session_state.bookmarks
            is_current = i == ci

            if is_current:
                icon = "●"
                color = "#63b3ed"
            elif is_answered:
                icon = "✓" if is_right else "✗"
                color = "#68d391" if is_right else "#fc8181"
            elif is_bm:
                icon = "🔖"
                color = "#f6ad55"
            else:
                icon = str(i + 1)
                color = "#3d5a75"

            with map_cols[i % len(map_cols)]:
                if st.button(icon, key=f"map_{i}",
                             help=f"Q{i+1}" + (" (bookmarked)" if is_bm else ""),
                             use_container_width=True):
                    st.session_state.current_q = i
                    st.rerun()
