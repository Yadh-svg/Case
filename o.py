

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
# concepts = st.text_area("Key Concepts in Chapter", """...""")
# num_questions = st.number_input("Number of Case-Based Questions", min_value=1, max_value=20, value=2)
 
# # 🧩 Subpart Configuration Section
# st.markdown("### ⚙️ Subpart Configuration")
# num_subparts = st.number_input("Number of Subparts", min_value=1, max_value=6, value=3)
 
# dok_levels = []
# marks_per_subpart = []
 
# st.markdown("#### Configure Each Subpart Below:")
# for i in range(num_subparts):
#     subpart_label = chr(97 + i)  # 'a', 'b', 'c', ...
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
 
# # Optional: Display a summary
# st.markdown("### 🧮 Subpart Summary")
# for i in range(num_subparts):
#     st.write(f"**({chr(97 + i)})** → {dok_levels[i]}, {marks_per_subpart[i]} Mark(s)")
 
# # -------- NEW: build the dynamic subparts block --------
# subparts_lines = []
# # indent to match where {{SUBPARTS_SECTION}} sits in YAML (2 spaces before the dash is typical)
# indent = "  "
# for i in range(num_subparts):
#     label = chr(97 + i)
#     subparts_lines.append(f"{indent}- Part ({label}): [{marks_per_subpart[i]} Mark(s), {dok_levels[i]}]")
 
# subparts_block = "\n".join(subparts_lines)
# # -------------------------------------------------------
 
# # Fill the template with user inputs
# input_data = {
#     "Grade": grade,
#     "Curriculam": curriculum,  # matches YAML key spelling
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
 
# # ✅ Step 2 (NEW): Insert the dynamic subparts section
# prompt_filled = prompt_filled.replace("{{SUBPARTS_SECTION}}", subparts_block)
 
# # ⛔ REMOVE the old Step 2 & Step 3 that replaced {{DOK_a}}/{{Marks_a}} and cleaned extras
 
# token_counter = TokenCounter()
 
# def generate_openai(api_key, prompt):
#     try:
#         client = OpenAI(api_key=api_key)
#         response = client.chat.completions.create(
#             model="gpt-5",
#             messages=[
#                 {"role": "system", "content": "You are an expert CBSE Mathematics Case-Based Study generator for Grades 1–12."},
#                 {"role": "user", "content": prompt}
#             ],
#             seed=random.randint(1, 1000000)
#         )
#         # cost against the actual prompt sent
#         input_tokens = token_counter.count_tokens(prompt)
#         output = response.choices[0].message.content.strip()
#         output_tokens = token_counter.count_tokens(output)
#         cost_input, cost_output, total_cost = token_counter.estimate_cost(input_tokens, output_tokens)
#         return {
#             "ok": True,
#             "output": output,
#             "input_tokens": input_tokens,
#             "output_tokens": output_tokens,
#             "cost_input": cost_input,
#             "cost_output": cost_output,
#             "total_cost": total_cost
#         }
#     except Exception as e:
#         return {"ok": False, "error": f"⚠️ OpenAI Error: {e}"}
 
# # Button to Generate Output
# if st.button("🚀 Generate Case Study"):
#     if not openai_key:
#         st.error("Please enter your OpenAI API key.")
#     else:
#         with st.spinner("Generating high-quality Case-Based Questions..."):
#             result = generate_openai(openai_key, prompt_filled)
 
#         if not result.get("ok"):
#             st.error(result["error"])
#         else:
#             st.subheader("🧠 Generated Case Study Output")
#             st.markdown(result["output"], unsafe_allow_html=True)
 
#             st.subheader("💰Cost Estimation")
#             st.write(f"**Input Tokens:** {result['input_tokens']}")
#             st.write(f"**Output Tokens:** {result['output_tokens']}")
#             st.write(f"**Input Cost:** ${result['cost_input']:.4f}")
#             st.write(f"**Output Cost:** ${result['cost_output']:.4f}")
#             st.write(f"**Total Estimated Cost:** ${result['total_cost']:.4f}")
 
#             # with st.expander("🪶 View Raw Prompt Used"):
#             #     st.code(prompt_filled)





import streamlit as st
import requests
import base64
import yaml
import json
import random

# ---------------------------
# Load YAML Prompt Template
# ---------------------------
with open("prompts.yaml", "r", encoding="utf-8") as file:
    data = yaml.safe_load(file)

prompt_template = data["case_study_maths"]

# ---------------------------
# Streamlit UI
# ---------------------------
st.title("📘 NCERT Case Study Generator ")

openai_api_key = st.text_input("🔑 Enter your  API Key", type="password")

# ---------------------------
# Mode Selection
# ---------------------------
st.markdown("### ✳️ Choose Input Mode")
input_mode = st.radio(
    "Select how you want to provide input:",
    ["Manual Input", "Upload PDF"],
    horizontal=True
)

# ---------------------------
# Common Inputs
# ---------------------------
grade = st.number_input("Grade", min_value=1, max_value=12, value=10)
curriculum = st.text_input("Curriculum", "NCERT")
subject = st.selectbox("Subject", ["Maths"])
num_questions = st.number_input("Number of Case-Based Questions", min_value=1, max_value=20, value=2)

# ---------------------------
# Subpart Configuration
# ---------------------------
st.markdown("### ⚙️ Subpart Configuration")
num_subparts = st.number_input("Number of Subparts", min_value=1, max_value=6, value=3)

dok_levels = []
marks_per_subpart = []

st.markdown("#### Configure Each Subpart Below:")
for i in range(num_subparts):
    subpart_label = chr(97 + i)
    st.markdown(f"**Subpart ({subpart_label})**")
    col1, col2 = st.columns(2)
    with col1:
        dok_level = st.selectbox(
            f"DOK Level for Part ({subpart_label})",
            ["DOK 1", "DOK 2", "DOK 3"],
            key=f"dok_{i}",
        )
    with col2:
        marks = st.number_input(
            f"Marks for Part ({subpart_label})",
            min_value=1,
            max_value=10,
            value=1,
            key=f"marks_{i}",
        )
    dok_levels.append(dok_level)
    marks_per_subpart.append(marks)
    st.markdown("---")

# ---------------------------
# Conditional Inputs
# ---------------------------
chapter = None
concepts = None
uploaded_file = None
topic = None

if input_mode == "Manual Input":
    st.markdown("### 🧾 Chapter Details")
    chapter = st.text_input("Chapter / Unit", "Surface area and volume")
    topic = st.text_input("Topic(s)", "Volume of a Combination of Solids, Conversion of Solids")
    concepts = st.text_area("Key Concepts in Chapter", "Surface area, Volume, Shapes conversion etc.")

elif input_mode == "Upload PDF":
    st.markdown("### 📄 Upload PDF for Input")
    uploaded_file = st.file_uploader("Upload your NCERT PDF", type=["pdf"])
    topic = st.text_input("Topic(s)", "Solid shapes, Volumes, Real-world geometry")

# ---------------------------
# Prepare Subpart Section
# ---------------------------
subparts_lines = []
indent = "  "
for i in range(num_subparts):
    label = chr(97 + i)
    subparts_lines.append(f"{indent}- Part ({label}): [{marks_per_subpart[i]} Mark(s), {dok_levels[i]}]")
subparts_block = "\n".join(subparts_lines)

# ---------------------------
# Prepare Prompt
# ---------------------------
input_data = {
    "Grade": grade,
    "Curriculam": curriculum,
    "Subject": subject,
    "Topic": topic,
    "Number_of_questions": num_questions,
    "Number_of_subparts": num_subparts,
}
if input_mode == "Manual Input":
    input_data["Chapter"] = chapter
    input_data["Concepts"] = concepts
else:
    input_data["Chapter"] = ""
    input_data["Concepts"] = ""

prompt_filled = prompt_template
for key, value in input_data.items():
    prompt_filled = prompt_filled.replace(f"{{{{{key}}}}}", str(value))
prompt_filled = prompt_filled.replace("{{SUBPARTS_SECTION}}", subparts_block)

# ✅ Step 3: Add PDF context note after "## INPUT DETAILS:" section
if input_mode == "Upload PDF":
    insertion_note = "\nFor the context of the chapter, you can refer to the uploaded PDF (keep this in mind), and generate case base study (More details of how to make cbs questions are mentioned below) questions based on the topic given.Make scenario's instead of just giving figure\n"
    import re

    pattern = r"^\s*##\s*INPUT\s*DETAILS\s*:\s*$"
    match = re.search(pattern, prompt_filled, re.IGNORECASE | re.MULTILINE)

    if match:
        start = match.end()
        prompt_filled = prompt_filled[:start] + "\n" + insertion_note + prompt_filled[start:]
    else:
        prompt_filled += "\n" + insertion_note


# ---------------------------
# Generate Button
# ---------------------------
if st.button("🚀 Generate Case Study"):
    if not openai_api_key:
        st.error("⚠️ Please enter your OpenAI API key.")
        st.stop()

    if input_mode == "Upload PDF" and not uploaded_file:
        st.error("⚠️ Please upload a PDF file.")
        st.stop()

    # Build payload
    if input_mode == "Upload PDF":
        pdf_bytes = uploaded_file.read()
        base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
        payload = {
            "model": "gpt-5",
            "input": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_file",
                            "filename": uploaded_file.name,
                            "file_data": f"data:application/pdf;base64,{base64_pdf}",
                        },
                        {"type": "input_text", "text": prompt_filled},
                    ],
                }
            ],
        }
    else:
        payload = {"model": "gpt-5", "input": prompt_filled}

    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json",
    }

    with st.spinner("⏳ Generating case study..."):
        response = requests.post("https://api.openai.com/v1/responses", headers=headers, json=payload)

    if response.status_code != 200:
        st.error(f"API Error {response.status_code}: {response.text}")
        st.stop()

    data = response.json()

    # ---------------------------
    # Extract Output
    # ---------------------------
    output_text = ""
    for item in data.get("output", []):
        if item.get("type") == "message":
            for content in item.get("content", []):
                if content.get("type") in ["output_text", "text"]:
                    output_text = content["text"]
                    break

    # ---------------------------
    # Token Usage + Cost
    # ---------------------------
    usage = data.get("usage", {})
    input_tokens = usage.get("input_tokens", 0)
    input_token_details = usage.get("input_tokens_details", {})
    cached_tokens = input_token_details.get("cached_tokens", 0)

    output_tokens = usage.get("output_tokens", 0)
    output_token_details = usage.get("output_tokens_details", {})
    reasoning_tokens = output_token_details.get("reasoning_tokens", 0)

    total_tokens = usage.get("total_tokens", input_tokens + output_tokens)
    non_cached_input = input_tokens - cached_tokens

    # Pricing
    INPUT_COST_PER_M = 1.25
    CACHED_INPUT_COST_PER_M = 0.125
    OUTPUT_COST_PER_M = 10.00

    input_cost = (non_cached_input / 1_000_000) * INPUT_COST_PER_M
    cached_cost = (cached_tokens / 1_000_000) * CACHED_INPUT_COST_PER_M
    output_cost = (output_tokens / 1_000_000) * OUTPUT_COST_PER_M
    total_cost = input_cost + cached_cost + output_cost

    # ---------------------------
    # Display Results
    # ---------------------------
    st.subheader("✅ Generated Case Study")
    st.markdown(output_text)

    st.divider()
    st.subheader("🧮 Token Usage")
    st.markdown(f"""
    - **Input Tokens:** {input_tokens:,}  
      • Cached: {cached_tokens:,}  
      • Non-Cached: {non_cached_input:,}  
    - **Output Tokens:** {output_tokens:,}  
      • Reasoning: {reasoning_tokens:,}  
    - **Total Tokens:** {total_tokens:,}
    """)

    st.divider()
    st.subheader("💰 Cost Breakdown (USD)")
    st.markdown(f"""
    | Type | Tokens | Rate (per 1M) | Cost (USD) |
    |------|---------|---------------|-------------|
    | Input (non-cached) | {non_cached_input:,} | ${INPUT_COST_PER_M} | **${input_cost:.6f}** |
    | Cached Input | {cached_tokens:,} | ${CACHED_INPUT_COST_PER_M} | **${cached_cost:.6f}** |
    | Output | {output_tokens:,} | ${OUTPUT_COST_PER_M} | **${output_cost:.6f}** |
    | **Total** | {total_tokens:,} | — | **${total_cost:.6f}** |
    """)

    st.divider()
    st.subheader("🧩 Raw Prompt Sent to Model")
    st.code(json.dumps(payload, indent=2), language="json")

    st.divider()
    st.subheader("🧾 Raw API Response")
    st.code(json.dumps(data, indent=2), language="json")
