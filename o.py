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
grade = st.number_input("Grade", min_value=1, max_value=12, value=10)
curriculum = st.text_input("Curriculum", "NCERT")
subject = st.selectbox("Subject", ["Maths"])
chapter = st.text_input("Chapter / Unit", "Surface area and volume")
topic = st.text_input("Topic(s)", "  Volume of a Combination of Solids,   Conversion of Solid from One Shape to Another")
concepts = st.text_area("Key Concepts in Chapter", 
                        """.Topics_Covered: Old Concepts (Recap from Earlier Classes) and New Concepts
Chapter_Description: |
  The chapter builds upon the foundational knowledge of 3D shapes that you learned in earlier grades (like Class 9).
 
Old_Concepts_Recap: |
  These are the fundamental concepts and formulas for individual solids that you are expected to recall and use:
 
  Individual Solids: Calculating the Curved/Lateral Surface Area (CSA/LSA), Total Surface Area (TSA), and Volume for the basic 3D shapes:
    - Cuboid (including Cube as a special case)
    - Cylinder (Right Circular Cylinder)
    - Cone (Right Circular Cone, including the relation l² = r² + h² for slant height)
    - Sphere
    - Hemisphere
 
New_Concepts: |
  The Class 10 curriculum primarily introduces the application of these formulas to more complex scenarios:
 
  Surface Area of a Combination of Solids:
    - Calculating the TSA or CSA of a solid that is formed by joining two or more basic solids (e.g., a toy which is a cone mounted on a hemisphere, or a vessel that is a cylinder with a hemispherical base).
    - The key here is to calculate the surface areas of the exposed parts only and sum them up, remembering that the area where the two solids join is not included in the total surface area of the combined solid.
 
  Volume of a Combination of Solids:
    - Calculating the total volume of a solid formed by combining two or more basic solids.
    - Unlike surface area, the volume of a composite solid is simply the sum of the volumes of its constituent solids.
 
  Conversion of Solid from One Shape to Another:
    - Solving problems where a solid (or combination of solids) is melted and recast into a new shape.
    - The core principle here is the conservation of volume: the Volume of the original solid(s) is equal to the Volume of the new solid(s) formed.
 
  Frustum of a Cone (Often an important concept, though sometimes rationalized out of the latest syllabus):
    - This is the portion of a cone left when a plane cuts it parallel to the base and the small cone formed on the top is removed (like a bucket).
    - Formulas for its Curved Surface Area, Total Surface Area, and Volume.
    - The focus is less on deriving the basic formulas and more on applying them to solve real-life problems involving combined and converted shapes.""")
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
