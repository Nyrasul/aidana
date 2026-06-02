import streamlit as st
import json
import random

@st.cache_data
def load_data():
    # Fallback mock data structure if the file isn't populated yet
    try:
        with open("questions.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return [
            {"question": "Sample Question 1?", "options": ["A", "B", "C"], "correct_answer": "A", "source": "File_A"},
            {"question": "Sample Question 2?", "options": ["A", "B", "C"], "correct_answer": "B", "source": "File_B"}
        ]

questions = load_data()

# --- PROGRESS TRACKING INITIALIZATION ---
if 'learned_questions' not in st.session_state:
    st.session_state.learned_questions = []  # Stores unique question strings that are mastered
if 'test_submitted' not in st.session_state:
    st.session_state.test_submitted = False

# --- SIDEBAR: PROGRESS & CONFIGURATION ---
st.sidebar.header("🎯 Test Configuration")

# Visual Progress Tracker Dashboard
total_pool_size = len(questions)
mastered_size = len(st.session_state.learned_questions)
progress_ratio = mastered_size / total_pool_size if total_pool_size > 0 else 0

st.sidebar.subheader("📈 Mastery Progress")
st.sidebar.progress(progress_ratio)
st.sidebar.write(f"**{mastered_size}** / **{total_pool_size}** questions fully learned ({int(progress_ratio * 100)}%)")

if mastered_size > 0:
    if st.sidebar.button("🗑️ Reset All Progress"):
        st.session_state.learned_questions = []
        st.rerun()

st.sidebar.write("---")

# Source Filtering
sources = list(set([q.get('source', 'Unknown') for q in questions]))
selected_sources = st.sidebar.multiselect("Select Files to Include:", sources, default=sources)
filtered_questions = [q for q in questions if q.get('source', 'Unknown') in selected_sources]

# Smart Smart Filter Option
exclude_learned = st.sidebar.checkbox("Exclude Mastered Questions", value=True, 
                                      help="Hides questions you have already answered correctly on previous tests.")

if exclude_learned:
    filtered_questions = [q for q in filtered_questions if q['question'] not in st.session_state.learned_questions]

max_q = len(filtered_questions)
if max_q > 0:
    num_q = st.sidebar.slider("Number of Questions:", 1, max_q, min(20, max_q))
    if st.sidebar.button("🚀 Start New Test"):
        st.session_state.quiz_data = random.sample(filtered_questions, num_q)
        st.session_state.current_q = 0
        st.session_state.user_answers = {}
        st.session_state.show_results = False
        st.session_state.failed_questions = []
        st.session_state.test_submitted = False  # Reset submission flag
        st.rerun()
else:
    if exclude_learned and len([q for q in questions if q.get('source', 'Unknown') in selected_sources]) > 0:
        st.sidebar.success("🎉 Incredible! You have mastered every question in this category. Uncheck 'Exclude Mastered' or reset progress to study them again.")
    else:
        st.sidebar.warning("No questions match your selection.")

# --- MAIN QUIZ UI ---
if 'quiz_data' not in st.session_state:
    st.title("⚕️ Medical Prep Quiz")
    st.info("Configure your test in the sidebar and click 'Start New Test'.")
else:
    q_data = st.session_state.quiz_data[st.session_state.current_q]
    
    st.subheader(f"Question {st.session_state.current_q + 1} / {len(st.session_state.quiz_data)}")
    st.write(q_data['question'])
    
    if q_data.get("images"):
        for img in q_data["images"]: 
            st.image(img, use_container_width=True)

    # Radio Selection
    ans = st.radio("Choose:", q_data['options'], key=f"q_{st.session_state.current_q}")
    st.session_state.user_answers[st.session_state.current_q] = ans

    # --- FEEDBACK LOGIC ---
    if st.button("Check Answer"):
        st.session_state.show_results = True
        
    if st.session_state.get('show_results', False):
        if st.session_state.user_answers[st.session_state.current_q] == q_data['correct_answer']:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect! Correct answer: {q_data['correct_answer']}")

    # Navigation
    c1, c2 = st.columns(2)
    if c1.button("⬅️ Previous") and st.session_state.current_q > 0:
        st.session_state.current_q -= 1
        st.session_state.show_results = False
        st.rerun()
    if c2.button("Next ➡️") and st.session_state.current_q < len(st.session_state.quiz_data) - 1:
        st.session_state.current_q += 1
        st.session_state.show_results = False
        st.rerun()

    # --- SUBMIT & EVALUATION LOGIC ---
    if st.session_state.current_q == len(st.session_state.quiz_data) - 1:
        st.write("---")
        
        if not st.session_state.test_submitted:
            if st.button("🏁 Submit Test"):
                st.session_state.failed_questions = []
                
                # Evaluate entire test runtime metrics
                for i, q in enumerate(st.session_state.quiz_data):
                    if st.session_state.user_answers.get(i) == q['correct_answer']:
                        # Add to mastered if it isn't already present
                        if q['question'] not in st.session_state.learned_questions:
                            st.session_state.learned_questions.append(q['question'])
                    else:
                        st.session_state.failed_questions.append(q)
                        # Penalty clause: if they learned it before but failed it now, remove it
                        if q['question'] in st.session_state.learned_questions:
                            st.session_state.learned_questions.remove(q['question'])
                            
                st.session_state.test_submitted = True
                st.rerun()
        else:
            # Display results panel after submission
            score = len(st.session_state.quiz_data) - len(st.session_state.failed_questions)
            st.metric("Final Score", f"{score} / {len(st.session_state.quiz_data)}")
            
            if st.session_state.failed_questions:
                st.warning(f"You missed {len(st.session_state.failed_questions)} questions. These have been updated in your profile.")
                
                if st.button("🔄 Retest Failed Questions"):
                    st.session_state.quiz_data = st.session_state.failed_questions
                    st.session_state.current_q = 0
                    st.session_state.user_answers = {}
                    st.session_state.show_results = False
                    st.session_state.failed_questions = []
                    st.session_state.test_submitted = False
                    st.rerun()
            else:
                st.success("🎉 Perfect score! Every question in this batch has been added to your Mastered list.")
