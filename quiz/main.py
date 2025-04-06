import streamlit as st
from dotenv import load_dotenv
import os
from quiz.chat_utils import generate_quiz
from quiz.html_generator import _format_quiz_with_reveal
import streamlit.components.v1 as components

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("GROQ_API_KEY not set in .env file.")

# Streamlit page setup
st.set_page_config(page_title="AI Quiz Generator", layout="wide")
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>AI-Powered Quiz Generator</h1>", unsafe_allow_html=True)

# Sidebar for user inputs
with st.sidebar:
    st.header("🛠️ Quiz Settings")
    topic = st.text_input("Enter Topic", value="Python")
    difficulty = st.selectbox("Select Difficulty", ["easy", "medium", "hard", "mixed"])
    num_questions = st.slider("Number of Questions", 1, 20, 5)
    if st.button("🚀 Generate Quiz"):
        with st.spinner("Generating quiz using ChatGroq..."):
            quiz = generate_quiz(topic, difficulty, num_questions)
            st.session_state["quiz"] = quiz

# Display quiz if available
if "quiz" in st.session_state and st.session_state["quiz"]:
    quiz_html = _format_quiz_with_reveal(st.session_state["quiz"])
    components.html(quiz_html, height=1200, scrolling=True)
