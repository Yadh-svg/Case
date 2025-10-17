import streamlit as st
from openai import OpenAI
import yaml

# Load YAML prompt
with open('prompts.yaml', 'r', encoding='utf-8') as file:
    data = yaml.safe_load(file)

prompt_template = data['case_study_maths']

# Streamlit UI
st.title("📘 NCERT Case Study Generator (OpenAI)")

# API Key
openai_key = st.text_input("🔑 OpenAI API Key", type="password")

# User Inputs
grade = st.number_input("Grade", min_value=1, max_value=12, value=8)
curriculum = st.text_input("Curriculum", "NCERT")
subject = st.selectbox("Subject", ["Maths"])
chapter = st.text_input("Chapter / Unit", "Mensuration")
topic = st.text_input("Topic(s)", "Spheres, Cones")
concepts = st.text_area("Key Concepts in Chapter", 
                        "Apply formulas for surface area and volume of solids, "
                        "combine multiple solids, compute curved surface area, etc.")
num_questions = st.number_input("Number of Case-Based Questions", min_value=1, max_value=20, value=2)

# Fill the template with user inputs
input_data = {
    "Grade": grade,
    "Curriculam": curriculum,
    "Subject": subject,
    "Chapter": chapter,
    "Topic": topic,
    "Concepts": concepts,
    "Number_of_questions": num_questions
}

prompt_filled = prompt_template
for key, value in input_data.items():
    prompt_filled = prompt_filled.replace(f"{{{{{key}}}}}", str(value))

# Generate Case Study Function
def generate_openai(api_key, prompt):
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "You are an expert CBSE Mathematics Case-Based Study generator for Grades 1–12."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ OpenAI Error: {e}"

# Button to Generate Output
if st.button("🚀 Generate Case Study"):
    if not openai_key:
        st.error("Please enter your OpenAI API key.")
    else:
        with st.spinner("Generating high-quality Case-Based Questions..."):
            output = generate_openai(openai_key, prompt_filled)

        # Display formatted output
        st.subheader("🧠 Generated Case Study Output")
        st.markdown(output, unsafe_allow_html=True)

        # Optional raw view
        with st.expander("🪶 View Raw Prompt Used"):
            st.code(prompt_filled)
