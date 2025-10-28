# import streamlit as st
# from openai import OpenAI
# import yaml
# import random
# from cost import TokenCounter
# # Load YAML prompt
# with open('prompts.yaml', 'r', encoding='utf-8') as file:
#     data = yaml.safe_load(file)

# prompt_template = data['case_study_maths']

# # Streamlit UI
# st.title("📘 NCERT Case Study Generator")

# # API Key
# openai_key = st.text_input("API Key", type="password")

# # User Inputs
# grade = st.number_input("Grade", min_value=1, max_value=12, value=10)
# curriculum = st.text_input("Curriculum", "NCERT")
# subject = st.selectbox("Subject", ["Maths"])
# chapter = st.text_input("Chapter / Unit", "Surface area and volume")
# topic = st.text_input("Topic(s)", "  Volume of a Combination of Solids,   Conversion of Solid from One Shape to Another")
# concepts = st.text_area("Key Concepts in Chapter", 
#                         """.Topics_Covered: Old Concepts (Recap from Earlier Classes) and New Concepts
# Chapter_Description: |
#   The chapter builds upon the foundational knowledge of 3D shapes that you learned in earlier grades (like Class 9).
 
# Old_Concepts_Recap: |
#   These are the fundamental concepts and formulas for individual solids that you are expected to recall and use:
 
#   Individual Solids: Calculating the Curved/Lateral Surface Area (CSA/LSA), Total Surface Area (TSA), and Volume for the basic 3D shapes:
#     - Cuboid (including Cube as a special case)
#     - Cylinder (Right Circular Cylinder)
#     - Cone (Right Circular Cone, including the relation l² = r² + h² for slant height)
#     - Sphere
#     - Hemisphere
 
# New_Concepts: |
#   The Class 10 curriculum primarily introduces the application of these formulas to more complex scenarios:
 
#   Surface Area of a Combination of Solids:
#     - Calculating the TSA or CSA of a solid that is formed by joining two or more basic solids (e.g., a toy which is a cone mounted on a hemisphere, or a vessel that is a cylinder with a hemispherical base).
#     - The key here is to calculate the surface areas of the exposed parts only and sum them up, remembering that the area where the two solids join is not included in the total surface area of the combined solid.
 
#   Volume of a Combination of Solids:
#     - Calculating the total volume of a solid formed by combining two or more basic solids.
#     - Unlike surface area, the volume of a composite solid is simply the sum of the volumes of its constituent solids.
 
#   Conversion of Solid from One Shape to Another:
#     - Solving problems where a solid (or combination of solids) is melted and recast into a new shape.
#     - The core principle here is the conservation of volume: the Volume of the original solid(s) is equal to the Volume of the new solid(s) formed.
 
#   Frustum of a Cone (Often an important concept, though sometimes rationalized out of the latest syllabus):
#     - This is the portion of a cone left when a plane cuts it parallel to the base and the small cone formed on the top is removed (like a bucket).
#     - Formulas for its Curved Surface Area, Total Surface Area, and Volume.
#     - The focus is less on deriving the basic formulas and more on applying them to solve real-life problems involving combined and converted shapes.""")
# num_questions = st.number_input("Number of Case-Based Questions", min_value=1, max_value=20, value=2)
# # 🧩 Subpart Configuration Section
# st.markdown("### ⚙️ Subpart Configuration")

# # Step 1: Choose number of subparts
# num_subparts = st.number_input("Number of Subparts", min_value=1, max_value=6, value=3)

# # Step 2: Dynamic input for each subpart (DOK Level + Marks)
# dok_levels = []
# marks_per_subpart = []

# st.markdown("#### Configure Each Subpart Below:")
# for i in range(num_subparts):
#     subpart_label = chr(97 + i)  # 'a', 'b', 'c', etc.
#     st.markdown(f"**Subpart ({subpart_label})**")
    
#     col1, col2 = st.columns(2)
#     with col1:
#         dok_level = st.selectbox(
#             f"DOK Level for Part ({subpart_label})",
#             ["DOK 1", "DOK 2", "DOK 3"],
#             key=f"dok_{i}"
#         )
#     with col2:
#         marks = st.number_input(
#             f"Marks for Part ({subpart_label})",
#             min_value=1, max_value=10, value=1,
#             key=f"marks_{i}"
#         )

#     dok_levels.append(dok_level)
#     marks_per_subpart.append(marks)
#     st.markdown("---")

# # Optional: Display a summary for clarity
# st.markdown("### 🧮 Subpart Summary")
# for i in range(num_subparts):
#     st.write(f"**({chr(97 + i)})** → {dok_levels[i]}, {marks_per_subpart[i]} Mark(s)")

# # Fill the template with user inputs
# # Fill the template with user inputs
# input_data = {
#     "Grade": grade,
#     "Curriculam": curriculum,
#     "Subject": subject,
#     "Chapter": chapter,
#     "Topic": topic,
#     "Concepts": concepts,
#     "Number_of_questions": num_questions,
#     "Number_of_subparts": num_subparts
# }

# prompt_filled = prompt_template

# # ✅ Step 1: Replace the simple placeholders
# for key, value in input_data.items():
#     prompt_filled = prompt_filled.replace(f"{{{{{key}}}}}", str(value))

# # ✅ Step 2: Replace DOK and Marks placeholders dynamically
# for i in range(num_subparts):
#     label = chr(97 + i)  # 'a', 'b', 'c', etc.
#     prompt_filled = prompt_filled.replace(f"{{{{DOK_{label}}}}}", dok_levels[i])
#     prompt_filled = prompt_filled.replace(f"{{{{Marks_{label}}}}}", str(marks_per_subpart[i]))

# # ✅ Step 3: Clean up placeholders for subparts not used (e.g., d–f if only 2 chosen)
# for j in range(num_subparts, 6):
#     label = chr(97 + j)
#     prompt_filled = prompt_filled.replace(f"{{{{DOK_{label}}}}}", "")
#     prompt_filled = prompt_filled.replace(f"{{{{Marks_{label}}}}}", "")


# token_counter = TokenCounter()
# # Generate Case Study Function
# def generate_openai(api_key, prompt):
#     try:
#         client = OpenAI(api_key=api_key)
#         response = client.chat.completions.create(
#             model="gpt-5",
#             messages=[
#                 {"role": "system", "content": "You are an expert CBSE Mathematics Case-Based Study generator for Grades 1–12."},
#                 {"role": "user", "content": prompt}
#             ],
#             # Allows sampling from the top 90% of probable tokens
#             seed=random.randint(1, 1000000)
#         )
#         input_tokens = token_counter.count_tokens(prompt_filled)
#         output = response.choices[0].message.content.strip()
#         output_tokens =  token_counter.count_tokens(output)
#         cost_input, cost_output, total_cost = token_counter.estimate_cost(input_tokens, output_tokens)
#         return {
#             "output": output,
#             "input_tokens": input_tokens,
#             "output_tokens": output_tokens,
#             "cost_input": cost_input,
#             "cost_output": cost_output,
#             "total_cost": total_cost
#         }
#     except Exception as e:
#         return f"⚠️ OpenAI Error: {e}"

# # Button to Generate Output
# if st.button("🚀 Generate Case Study"):
#     if not openai_key:
#         st.error("Please enter your OpenAI API key.")
#     else:
#         with st.spinner("Generating high-quality Case-Based Questions..."):
#             output = generate_openai(openai_key, prompt_filled)

#         if "error" in output:
#               st.error(output["error"])
#         else:
#             st.subheader("🧠 Generated Case Study Output")
#             st.markdown(output["output"], unsafe_allow_html=True)

#             st.subheader("💰Cost Estimation")
#             st.write(f"**Input Tokens:** {output['input_tokens']}")
#             st.write(f"**Output Tokens:** {output['output_tokens']}")
#             st.write(f"**Input Cost:** ${output['cost_input']:.4f}")
#             st.write(f"**Output Cost:** ${output['cost_output']:.4f}")
#             st.write(f"**Total Estimated Cost:** ${output['total_cost']:.4f}")

#             with st.expander("🪶 View Raw Prompt Used"):
#                 st.code(prompt_filled)



import streamlit as st
from openai import OpenAI
import yaml
import random
from cost import TokenCounter
 
# Load YAML prompt
with open('prompts.yaml', 'r', encoding='utf-8') as file:
    data = yaml.safe_load(file)
 
prompt_template = data['case_study_maths']
 
# Streamlit UI
st.title("📘 NCERT Case Study Generator")
 
# API Key
openai_key = st.text_input("API Key", type="password")
 
# User Inputs
grade = st.number_input("Grade", min_value=1, max_value=12, value=10)
curriculum = st.text_input("Curriculum", "NCERT")
subject = st.selectbox("Subject", ["Maths"])
chapter = st.text_input("Chapter / Unit", "Surface area and volume")
topic = st.text_input("Topic(s)", "  Volume of a Combination of Solids,   Conversion of Solid from One Shape to Another")
concepts = st.text_area("Key Concepts in Chapter", """...""")
num_questions = st.number_input("Number of Case-Based Questions", min_value=1, max_value=20, value=2)
 
# 🧩 Subpart Configuration Section
st.markdown("### ⚙️ Subpart Configuration")
num_subparts = st.number_input("Number of Subparts", min_value=1, max_value=6, value=3)
 
dok_levels = []
marks_per_subpart = []
 
st.markdown("#### Configure Each Subpart Below:")
for i in range(num_subparts):
    subpart_label = chr(97 + i)  # 'a', 'b', 'c', ...
    st.markdown(f"**Subpart ({subpart_label})**")
    col1, col2 = st.columns(2)
    with col1:
        dok_level = st.selectbox(
            f"DOK Level for Part ({subpart_label})",
            ["DOK 1", "DOK 2", "DOK 3"],
            key=f"dok_{i}"
        )
    with col2:
        marks = st.number_input(
            f"Marks for Part ({subpart_label})",
            min_value=1, max_value=10, value=1,
            key=f"marks_{i}"
        )
    dok_levels.append(dok_level)
    marks_per_subpart.append(marks)
    st.markdown("---")
 
# Optional: Display a summary
st.markdown("### 🧮 Subpart Summary")
for i in range(num_subparts):
    st.write(f"**({chr(97 + i)})** → {dok_levels[i]}, {marks_per_subpart[i]} Mark(s)")
 
# -------- NEW: build the dynamic subparts block --------
subparts_lines = []
# indent to match where {{SUBPARTS_SECTION}} sits in YAML (2 spaces before the dash is typical)
indent = "  "
for i in range(num_subparts):
    label = chr(97 + i)
    subparts_lines.append(f"{indent}- Part ({label}): [{marks_per_subpart[i]} Mark(s), {dok_levels[i]}]")
 
subparts_block = "\n".join(subparts_lines)
# -------------------------------------------------------
 
# Fill the template with user inputs
input_data = {
    "Grade": grade,
    "Curriculam": curriculum,  # matches YAML key spelling
    "Subject": subject,
    "Chapter": chapter,
    "Topic": topic,
    "Concepts": concepts,
    "Number_of_questions": num_questions,
    "Number_of_subparts": num_subparts
}
 
prompt_filled = prompt_template
 
# ✅ Step 1: Replace the simple placeholders
for key, value in input_data.items():
    prompt_filled = prompt_filled.replace(f"{{{{{key}}}}}", str(value))
 
# ✅ Step 2 (NEW): Insert the dynamic subparts section
prompt_filled = prompt_filled.replace("{{SUBPARTS_SECTION}}", subparts_block)
 
# ⛔ REMOVE the old Step 2 & Step 3 that replaced {{DOK_a}}/{{Marks_a}} and cleaned extras
 
token_counter = TokenCounter()
 
def generate_openai(api_key, prompt):
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "You are an expert CBSE Mathematics Case-Based Study generator for Grades 1–12."},
                {"role": "user", "content": prompt}
            ],
            seed=random.randint(1, 1000000)
        )
        # cost against the actual prompt sent
        input_tokens = token_counter.count_tokens(prompt)
        output = response.choices[0].message.content.strip()
        output_tokens = token_counter.count_tokens(output)
        cost_input, cost_output, total_cost = token_counter.estimate_cost(input_tokens, output_tokens)
        return {
            "ok": True,
            "output": output,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost_input": cost_input,
            "cost_output": cost_output,
            "total_cost": total_cost
        }
    except Exception as e:
        return {"ok": False, "error": f"⚠️ OpenAI Error: {e}"}
 
# Button to Generate Output
if st.button("🚀 Generate Case Study"):
    if not openai_key:
        st.error("Please enter your OpenAI API key.")
    else:
        with st.spinner("Generating high-quality Case-Based Questions..."):
            result = generate_openai(openai_key, prompt_filled)
 
        if not result.get("ok"):
            st.error(result["error"])
        else:
            st.subheader("🧠 Generated Case Study Output")
            st.markdown(result["output"], unsafe_allow_html=True)
 
            st.subheader("💰Cost Estimation")
            st.write(f"**Input Tokens:** {result['input_tokens']}")
            st.write(f"**Output Tokens:** {result['output_tokens']}")
            st.write(f"**Input Cost:** ${result['cost_input']:.4f}")
            st.write(f"**Output Cost:** ${result['cost_output']:.4f}")
            st.write(f"**Total Estimated Cost:** ${result['total_cost']:.4f}")
 
            # with st.expander("🪶 View Raw Prompt Used"):
            #     st.code(prompt_filled)