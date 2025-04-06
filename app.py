import streamlit as st
from helper import get_youtube_urls,embed_codes,chat
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
st.set_page_config(page_title= "🧠AI-Powered Learning Hub", layout="wide")
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🤖📘AI-Powered Learning Hub 📘🤖</h1>", unsafe_allow_html=True)

tab1, tab2, tab3,tab4 = st.tabs([ "🧠 Quiz","🎬 Video Resources","📄 Notes","🤖 Chat bot"])
# First tab content
query=st.sidebar.text_input("**Enter the Topic**")
with tab1:
    
    with st.sidebar:
        st.header("🛠️ Quiz Settings")
        # topic = st.text_input("Enter Topic", value="Python")
        difficulty = st.selectbox("Select Difficulty", ["easy", "medium", "hard", "mixed"])
        num_questions = st.slider("Number of Questions", 1, 20, 5)
        if st.button("🚀 Generate Quiz"):
            with st.spinner(f"Generating quiz on {query}..."):
                quiz = generate_quiz(query, difficulty, num_questions)
                st.session_state["quiz"] = quiz

        # Display quiz if available
    if "quiz" in st.session_state and st.session_state["quiz"]:
        quiz_html = _format_quiz_with_reveal(st.session_state["quiz"])
        components.html(quiz_html, height=1200, scrolling=True)
with tab2:
    st.header(f"🎬 Video Resources on {query}")
    urls=get_youtube_urls(query)
    iframe_list=embed_codes(urls)
    cols = st.columns(3)
    for idx, iframe in enumerate(iframe_list):
        with cols[idx % 3]:  # Distribute across columns
            st.components.v1.html(iframe, height=340)


with tab3:
    st.header("📄 Notes")
    prompt="""[System Prompt]
    You are an expert teacher and AI assistant that explains complex topics in a simple and structured way. You provide a step-by-step breakdown of topics, starting from beginner-friendly concepts to more advanced explanations. Always use clear, easy-to-understand language, analogies when needed, and examples or code if applicable.

    Format your answer in the following structure:
    1. **Introduction** – Give a short overview of the topic.
    2. **Basic Explanation** – Start with a beginner-level explanation.
    3. **Intermediate Concepts** – Build upon the basics with a deeper explanation.
    4. **Advanced Understanding** – Cover technical or advanced aspects in detail.
    5. **Examples** – Provide examples, diagrams, or code snippets where appropriate.
    6. **Real-world Applications** – Mention how and where this topic is used.
    7. **Summary** – Recap the topic in a concise way.

    Only explain what is asked. Don’t include unrelated information. Be patient and pedagogical in your tone.

    ---

    [User Prompt]
    Explain the topic: "{query}"

    Make sure to follow the structure from introduction to summary. Include relevant examples, analogies, and applications if possible."""

    st.success(chat(query))


with tab4:
    st.header("🤖 Chat bot")
    input=st.text_input("**Ask your queries:**")
    st.success(chat(input))


