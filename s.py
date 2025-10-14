import streamlit as st
from google import genai
import yaml

# Load YAML prompts
with open('prompts.yaml', 'r', encoding='utf-8') as file:
    data = yaml.safe_load(file)
prompt_template = data['case_study_maths']

# Streamlit UI
st.title("NCERT Case Study Generator (Markdown + LaTeX supported)")

# API key input (password type)
api_key = st.text_input("Enter your Google GenAI API Key", type="password")

grade = st.number_input("Grade", min_value=1, max_value=12, value=8)
chapter = st.text_input("Chapter", "1. Patterns in Mathematics")
topic = st.text_input("Topic", "Visualising Number Sequences")
num_questions = st.number_input("Number of Questions", min_value=1, max_value=20, value=4)
curriculum = st.text_input("Curriculum", "NCERT")
subject = st.selectbox("Subject", ["Maths", "Science"])

if st.button("Generate Case Study"):
    if not api_key:
        st.error("Please enter your API key to generate the case study.")
    else:
        input_data = {
            "Grade": grade,
            "Chapter": chapter,
            "Topic": topic,
            "Number_of_questions": num_questions,
            "Curriculam": curriculum,
            "Subject": subject
        }

        # Replace placeholders in prompt
        prompt_filled = prompt_template
        for key, value in input_data.items():
            prompt_filled = prompt_filled.replace(f"{{{{{key}}}}}", str(value))

        # Initialize GenAI client with user-provided API key
        client = genai.Client(api_key=api_key)

        # Generate response
        with st.spinner("Generating case study..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash-preview-09-2025",
                contents=prompt_filled
            )

        st.success("Case Study Generated!")

        # Render Markdown + LaTeX
        st.markdown(response.text, unsafe_allow_html=True)

        # Optional: show raw output for debugging
        with st.expander("Show Raw Output"):
            st.code(response.text)
