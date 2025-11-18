
# pages/o.py
import streamlit as st
import yaml
import time
import threading
import queue
import re
from google import genai
from google.genai import types
from openai import OpenAI

st.title("📝 Manual Case Study Generator")
if st.button("⬅ Back to Mode Selection"):
    st.switch_page("app.py")

# Model selection radio
model_choice = st.radio("Select Model", ["GPT-5 Only", "Gemini Only", "Both"], index=2)

# API keys shown based on model choice
OPENAI_API_KEY = ""
GEMINI_API_KEY = ""
if model_choice in ("GPT-5 Only", "Both"):
    OPENAI_API_KEY = st.text_input("OpenAI API Key (GPT-5)", type="password")
if model_choice in ("Gemini Only", "Both"):
    GEMINI_API_KEY = st.text_input("Gemini API Key", type="password")

st.divider()

# load prompt template
prompt_template = None
try:
    with open("prompts.yaml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    prompt_template = data.get("case_study_maths")
    if not prompt_template:
        st.error("prompts.yaml missing 'case_study_maths'.")
except FileNotFoundError:
    st.error("prompts.yaml not found.")
except Exception as e:
    st.error(f"Error loading prompts.yaml: {e}")

# Manual inputs
grade = st.number_input("Grade", 1, 12, 10)
curriculum = st.text_input("Curriculum", "NCERT")
subject = st.selectbox("Subject", ["Maths"])
num_questions = st.number_input("Number of Case-Based Questions", 1, 20, 2)
num_subparts = st.number_input("Number of Subparts", 1, 6, 3)

dok_levels = []
marks_per_subpart = []
for i in range(num_subparts):
    label = chr(97 + i)
    col1, col2 = st.columns(2)
    with col1:
        dok = st.selectbox(f"DOK Level ({label})", ["DOK 1", "DOK 2", "DOK 3"], key=f"dok_o_{i}")
    with col2:
        marks = st.number_input(f"Marks ({label})", 1, 10, 1, key=f"marks_o_{i}")
    dok_levels.append(dok)
    marks_per_subpart.append(marks)

subparts_block = "\n".join([
    f"  - Part ({chr(97 + i)}): [{marks_per_subpart[i]} Mark(s), {dok_levels[i]}]"
    for i in range(num_subparts)
])

chapter = st.text_input("Chapter / Unit", "Surface area and volume")
topic = st.text_input("Topic(s)", "Volume of a Combination of Solids")
concepts = st.text_area("Key Concepts", "Surface area, Volume, Shapes conversion etc.")

input_data = {
    "Grade": grade,
    "Curriculam": curriculum,
    "Subject": subject,
    "Topic": topic,
    "Number_of_questions": num_questions,
    "Number_of_subparts": num_subparts,
    "Chapter": chapter,
    "Concepts": concepts,
}

def build_prompt(template, mapping, subparts_text):
    if not template:
        return None
    out = template
    for k, v in mapping.items():
        pattern = re.compile(r"\{\{\s*" + re.escape(k) + r"\s*\}\}", re.IGNORECASE)
        out = pattern.sub(str(v), out)
    out = out.replace("{{SUBPARTS_SECTION}}", subparts_text)
    return out

final_prompt = build_prompt(prompt_template, input_data, subparts_block)
# if final_prompt:
#     with st.expander("Preview final prompt"):
#         st.code(final_prompt[:10000])

st.markdown("---")

# UI placeholders - conditional
if model_choice in ("Both", "Gemini Only"):
    gemini_timer = st.empty()
    gemini_output = st.empty()
if model_choice in ("Both", "GPT-5 Only"):
    gpt_timer = st.empty()
    gpt_output = st.empty()
status = st.empty()

# Threading functions
def run_gemini_stream(prompt, api_key, q, done_flag, result_store):
    start = time.time()
    try:
        client = genai.Client(api_key=api_key)
        config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(include_thoughts=False, thinking_budget=3000)
        )
        stream = client.models.generate_content_stream(model="gemini-2.5-pro", contents=[prompt], config=config)
        for chunk in stream:
            txt = getattr(chunk, "text", "") or ""
            if txt:
                q.put(txt)
    except Exception as e:
        q.put(f"[Gemini Error] {e}")
    finally:
        q.put(None)
        result_store["elapsed"] = time.time() - start
        done_flag.set()

def run_gpt(prompt, api_key, result_store, done_flag):
    start = time.time()
    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(model="gpt-5", input=prompt)
        text = getattr(response, "output_text", None)
        if text is None:
            try:
                text = response.output[0].content[0].text
            except Exception:
                text = str(response)
        result_store["text"] = text
    except Exception as e:
        result_store["text"] = f"[GPT-5 Error] {e}"
    finally:
        result_store["elapsed"] = time.time() - start
        done_flag.set()

# Run button
if st.button("🚀 Generate"):
    # validation
    if model_choice in ("Both", "GPT-5 Only") and (not OPENAI_API_KEY):
        st.error("OpenAI API key required.")
    elif model_choice in ("Both", "Gemini Only") and (not GEMINI_API_KEY):
        st.error("Gemini API key required.")
    else:
        gemini_enabled = model_choice in ("Both", "Gemini Only")
        gpt_enabled = model_choice in ("Both", "GPT-5 Only")
        gemini_q = queue.Queue()
        gemini_done = threading.Event()
        gpt_done = threading.Event()
        gemini_result = {"text": "", "elapsed": None}
        gpt_result = {"text": "", "elapsed": None}

        # start threads selectively
        if gemini_enabled:
            threading.Thread(
                target=run_gemini_stream,
                args=(final_prompt, GEMINI_API_KEY, gemini_q, gemini_done, gemini_result),
                daemon=True
            ).start()
            gemini_start = time.time()
        if gpt_enabled:
            threading.Thread(
                target=run_gpt,
                args=(final_prompt, OPENAI_API_KEY, gpt_result, gpt_done),
                daemon=True
            ).start()
            gpt_start = time.time()

        status.info("Started...")

        # polling loop
        aggregated = ""
        first_shown = None
        while True:
            if gemini_enabled and not gemini_done.is_set():
                gemini_timer.write(f"Gemini Time: {time.time()-gemini_start:.1f}s")
            if gpt_enabled and not gpt_done.is_set():
                gpt_timer.write(f"GPT-5 Time: {time.time()-gpt_start:.1f}s")

            if gemini_enabled:
                try:
                    chunk = gemini_q.get_nowait()
                    if chunk is None:
                        pass
                    else:
                        aggregated += chunk
                        if first_shown is None:
                            first_shown = "gemini"
                            gemini_output.markdown("### 🟦 Gemini (streaming)")
                        gemini_output.markdown(aggregated, unsafe_allow_html=True)
                except queue.Empty:
                    pass

            if gpt_enabled and gpt_done.is_set() and first_shown is None:
                first_shown = "gpt"
                gpt_output.markdown("### 🟥 GPT-5 (final)")
                gpt_output.text(gpt_result["text"])

            both_done = True
            if gemini_enabled and not gemini_done.is_set():
                both_done = False
            if gpt_enabled and not gpt_done.is_set():
                both_done = False
            if both_done:
                break

            time.sleep(0.1)

        # final rendering
        if gemini_enabled:
            gemini_timer.write(f"Gemini Time: {gemini_result['elapsed']:.2f}s")
            if first_shown != "gemini":
                gemini_output.markdown("### 🟦 Gemini (final)")
                gemini_output.markdown(gemini_result["text"], unsafe_allow_html=True)
        if gpt_enabled:
            gpt_timer.write(f"GPT-5 Time: {gpt_result['elapsed']:.2f}s")
            if first_shown != "gpt":
                gpt_output.markdown("### 🟥 GPT-5 (final)")
                gpt_output.text(gpt_result["text"])

        status.success("Done 🎉")
