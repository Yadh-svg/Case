# # # from google import genai
# # # from google.genai import types
# # # import pathlib

# # # client = genai.Client(api_key="AIzaSyC-PvEwQkBqZTQbON6eqe-ZHn5gJR-E2S8")

# # # # Retrieve and encode the PDF byte
# # # filepath = pathlib.Path(r'C:\Users\trial\projects\in_git\CASE_STUDY_MYGIT\Case\Supercells.pdf')

# # # prompt = "Summarize this document"
# # # response = client.models.generate_content(
# # #   model="gemini-2.5-flash",
# # #   contents=[
# # #       types.Part.from_bytes(
# # #         data=filepath.read_bytes(),
# # #         mime_type='application/pdf',
# # #       ),
# # #       prompt])
# # # print(response.text)

# # import streamlit as st
# # import yaml
# # import time
# # from google import genai
# # from google.genai import types
# # import queue
# # import threading

# # # ---------------------------------------------------------
# # # UI: API Key
# # # ---------------------------------------------------------
# # st.title("📘 NCERT Case Study Generator (Gemini Streaming)")

# # GEMINI_API_KEY = st.text_input("Gemini API Key", type="password")
# # st.divider()

# # # ---------------------------------------------------------
# # # Load YAML prompt template
# # # ---------------------------------------------------------
# # with open("prompts.yaml", "r", encoding="utf-8") as f:
# #     data = yaml.safe_load(f)

# # prompt_template = data["case_study_maths"]

# # # ---------------------------------------------------------
# # # PDF Upload
# # # ---------------------------------------------------------
# # uploaded_pdf = st.file_uploader("Upload Chapter PDF", type=["pdf"])

# # # ---------------------------------------------------------
# # # Inputs (same as before except Concepts removed)
# # # ---------------------------------------------------------
# # st.subheader("Problem Configuration")

# # grade = st.number_input("Grade", 1, 12, 10)
# # curriculum = st.text_input("Curriculum", "NCERT")
# # subject = st.selectbox("Subject", ["Maths"])
# # num_questions = st.number_input("Number of Questions", 1, 20, 2)

# # chapter = st.text_input("Chapter / Unit", "Surface area and volume")
# # topic = st.text_input("Topic(s)", "Volume of Combination of Solids")

# # # New Inputs
# # old_concepts = st.text_area("Old Concept", "Surface area, Volume, Shapes etc.")
# # additional_note = st.text_area("Additional Note for Solutions", 
# #                                "Ensure each solution includes unit conversions and diagrams where needed.")

# # # ---------------------------------------------------------
# # # Subpart Configuration
# # # ---------------------------------------------------------
# # st.subheader("Subpart Configuration")

# # num_subparts = st.number_input("Number of Subparts", 1, 6, 3)

# # dok_levels = []
# # marks_per_subpart = []

# # for i in range(num_subparts):
# #     label = chr(97 + i)
# #     col1, col2 = st.columns(2)
# #     with col1:
# #         dok = st.selectbox(f"DOK Level ({label})", ["DOK 1", "DOK 2", "DOK 3"], key=f"dok_{i}")
# #     with col2:
# #         marks = st.number_input(f"Marks ({label})", 1, 10, 1, key=f"marks_{i}")
# #     dok_levels.append(dok)
# #     marks_per_subpart.append(marks)

# # subparts_block = "\n".join([
# #     f"  - Part ({chr(97 + i)}): [{marks_per_subpart[i]} Mark(s), {dok_levels[i]}]"
# #     for i in range(num_subparts)
# # ])

# # # ---------------------------------------------------------
# # # Build final prompt
# # # ---------------------------------------------------------
# # input_data = {
# #     "Grade": grade,
# #     "Curriculam": curriculum,
# #     "Subject": subject,
# #     "Topic": topic,
# #     "Number_of_questions": num_questions,
# #     "Number_of_subparts": num_subparts,
# #     "Chapter": chapter,
# # }

# # prompt_filled = prompt_template
# # for key, value in input_data.items():
# #     prompt_filled = prompt_filled.replace(f"{{{{{key}}}}}", str(value))

# # prompt_filled = prompt_filled.replace("{{SUBPARTS_SECTION}}", subparts_block)

# # # Append new required sections
# # extra_block = f"""
# # Old concept: {old_concepts}

# # The PDF contains the key concepts of the chapter (see attached PDF).

# # Also follow this additional instruction strictly while generating the solution:
# # {additional_note}
# # """

# # final_prompt = prompt_filled + "\n\n" + extra_block

# # # ---------------------------------------------------------
# # # Streaming Output Handling
# # # ---------------------------------------------------------
# # output_box = st.empty()
# # status_box = st.empty()

# # def run_gemini_stream(pdf_bytes, prompt, api_key, output_queue, done_signal):
# #     client = genai.Client(api_key=api_key)

# #     pdf_part = types.Part.from_bytes(
# #         data=pdf_bytes,
# #         mime_type="application/pdf"
# #     )

# #     config = types.GenerateContentConfig(
# #         thinking_config=types.ThinkingConfig(
# #             include_thoughts=False,
# #             thinking_budget=3000
# #         )
# #     )

# #     try:
# #         stream = client.models.generate_content_stream(
# #             model="gemini-2.5-pro",
# #             contents=[pdf_part, prompt],
# #             config=config
# #         )

# #         for chunk in stream:
# #             text_chunk = getattr(chunk, "text", "")
# #             if text_chunk:
# #                 output_queue.put(text_chunk)

# #     except Exception as e:
# #         output_queue.put(f"[Error] {e}")

# #     finally:
# #         output_queue.put(None)
# #         done_signal.set()

# # # ---------------------------------------------------------
# # # Generate Button
# # # ---------------------------------------------------------
# # if st.button("🚀 Generate Case Study with Gemini"):
# #     if not GEMINI_API_KEY:
# #         st.error("Please enter Gemini API Key.")
# #     elif uploaded_pdf is None:
# #         st.error("Upload a PDF file.")
# #     else:
# #         output_queue = queue.Queue()
# #         done_signal = threading.Event()

# #         pdf_bytes = uploaded_pdf.read()

# #         # Start streaming thread
# #         thread = threading.Thread(
# #             target=run_gemini_stream,
# #             args=(pdf_bytes, final_prompt, GEMINI_API_KEY, output_queue, done_signal),
# #             daemon=True
# #         )
# #         thread.start()

# #         full_output = ""

# #         while not done_signal.is_set() or not output_queue.empty():
# #             try:
# #                 chunk = output_queue.get(timeout=0.1)
# #                 if chunk is None:
# #                     break
# #                 full_output += chunk
# #                 output_box.markdown(full_output)
# #             except queue.Empty:
# #                 pass

# #         status_box.success("✨ Generation Complete!")

# import streamlit as st
# import yaml
# import time
# import threading
# import queue
# from google import genai
# from google.genai import types
# from openai import OpenAI

# # ---------------------------------------------------------
# # UI: API Keys
# # ---------------------------------------------------------
# import streamlit as st

# if st.button("⬅ Back to Mode Selection"):
#     st.switch_page("app.py")

# st.title("📄 PDF Case Study Generator")

# # ... your full PDF code ...

# st.title("📘 NCERT Case Study Generator — Gemini + GPT-5 (Parallel)")

# OPENAI_API_KEY = st.text_input("OpenAI API Key", type="password")
# GEMINI_API_KEY = st.text_input("Gemini API Key", type="password")
# st.divider()

# # ---------------------------------------------------------
# # YAML template
# # ---------------------------------------------------------
# with open("prompts.yaml", "r", encoding="utf-8") as f:
#     data = yaml.safe_load(f)
# prompt_template = data["case_study_maths"]

# # ---------------------------------------------------------
# # File uploader
# # ---------------------------------------------------------
# uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])

# # ---------------------------------------------------------
# # User Inputs
# # ---------------------------------------------------------
# st.subheader("Case Study Configuration")

# grade = st.number_input("Grade", 1, 12, 10)
# curriculum = st.text_input("Curriculum", "NCERT")
# subject = st.text_input("Subject", "Maths")
# chapter = st.text_input("Chapter / Unit", "Surface area and volume")
# topic = st.text_input("Topic(s)", "Volume of a Combination of Solids")

# num_questions = st.number_input("Number of Questions", 1, 20, 2)
# num_subparts = st.number_input("Number of Subparts", 1, 6, 3)

# st.subheader("Old Concept + Additional Notes")

# old_concepts = st.text_area("Old Concept", "Surface area, Volume, Shapes etc.")
# additional_note = st.text_area("Additional Note for Solution",
#                                "Ensure steps are clear and units are consistent.")

# # ---------------------------------------------------------
# # Subpart Config
# # ---------------------------------------------------------
# st.subheader("Subparts")

# dok_levels = []
# marks_per_subpart = []

# for i in range(num_subparts):
#     label = chr(97 + i)
#     c1, c2 = st.columns(2)
#     with c1:
#         dok = st.selectbox(f"DOK ({label})", ["DOK 1", "DOK 2", "DOK 3"], key=f"dok_{i}")
#     with c2:
#         marks = st.number_input(f"Marks ({label})", 1, 10, 1, key=f"marks_{i}")
#     dok_levels.append(dok)
#     marks_per_subpart.append(marks)

# subparts_block = "\n".join([
#     f"  - Part ({chr(97+i)}): [{marks_per_subpart[i]} Mark(s), {dok_levels[i]}]"
#     for i in range(num_subparts)
# ])

# # ---------------------------------------------------------
# # Build final prompt
# # ---------------------------------------------------------
# input_data = {
#     "Grade": grade,
#     "Curriculam": curriculum,
#     "Subject": subject,
#     "Topic": topic,
#     "Number_of_questions": num_questions,
#     "Number_of_subparts": num_subparts,
#     "Chapter": chapter,
# }

# prompt_filled = prompt_template
# for key, val in input_data.items():
#     prompt_filled = prompt_filled.replace(f"{{{{{key}}}}}", str(val))

# prompt_filled = prompt_filled.replace("{{SUBPARTS_SECTION}}", subparts_block)

# extra_text = f"""
# Old concept: {old_concepts}

# The PDF contains the key concepts of the chapter (see attached PDF).

# Also follow this additional instruction strictly while generating the solution:
# {additional_note}
# """

# final_prompt = prompt_filled + "\n\n" + extra_text

# # ---------------------------------------------------------
# # Output placeholders
# # ---------------------------------------------------------
# colA, colB = st.columns([1, 1])
# with colA:
#     gemini_timer = st.empty()
# with colB:
#     gpt_timer = st.empty()

# first_title = st.empty()
# first_output = st.empty()
# second_title = st.empty()
# second_output = st.empty()
# status_box = st.empty()


# # ---------------------------------------------------------
# # Threads
# # ---------------------------------------------------------
# def run_gemini(pdf_bytes, prompt, key, q, done_flag, result_store):
#     client = genai.Client(api_key=key)

#     pdf_part = types.Part.from_bytes(
#         data=pdf_bytes,
#         mime_type="application/pdf"
#     )

#     config = types.GenerateContentConfig(
#         thinking_config=types.ThinkingConfig(
#             include_thoughts=False,
#             thinking_budget=3000
#         )
#     )

#     start = time.time()

#     try:
#         stream = client.models.generate_content_stream(
#             model="gemini-2.5-pro",
#             contents=[pdf_part, prompt],
#             config=config
#         )

#         for chunk in stream:
#             text_chunk = getattr(chunk, "text", "")
#             if text_chunk:
#                 q.put(text_chunk)

#     except Exception as e:
#         q.put(f"[Gemini Error] {e}")

#     finally:
#         q.put(None)
#         result_store["elapsed"] = time.time() - start
#         done_flag.set()


# def run_gpt(pdf_path, prompt, key, result_store, done_flag):
#     client = OpenAI(api_key=key)
#     start = time.time()
#     try:
#         # Upload file
#         file = client.files.create(
#             file=open(pdf_path, "rb"),
#             purpose="user_data"
#         )

#         # Ask GPT-5
#         response = client.responses.create(
#             model="gpt-5",
#             input=[
#                 {
#                     "role": "user",
#                     "content": [
#                         {"type": "input_file", "file_id": file.id},
#                         {"type": "input_text", "text": prompt},
#                     ]
#                 }
#             ]
#         )

#         # Get output text
#         result_store["text"] = response.output_text

#         # Delete file after use
#         client.files.delete(file.id)

#     except Exception as e:
#         result_store["text"] = f"[GPT-5 Error] {e}"

#     finally:
#         result_store["elapsed"] = time.time() - start
#         done_flag.set()


# # ---------------------------------------------------------
# # Generate Button
# # ---------------------------------------------------------
# if st.button("🚀 Run Both Models (Parallel)"):

#     if not OPENAI_API_KEY or not GEMINI_API_KEY:
#         st.error("Please enter both API keys.")
#     elif uploaded_pdf is None:
#         st.error("Please upload a PDF.")
#     else:
#         pdf_bytes = uploaded_pdf.read()

#         # Save PDF temporarily for GPT-5
#         temp_path = "temp_uploaded.pdf"
#         with open(temp_path, "wb") as f:
#             f.write(pdf_bytes)

#         # Shared structures
#         gemini_q = queue.Queue()
#         gemini_done = threading.Event()
#         gpt_done = threading.Event()
#         gemini_result = {"elapsed": None}
#         gpt_result = {"text": "", "elapsed": None}

#         # Start threads
#         threading.Thread(
#             target=run_gemini,
#             args=(pdf_bytes, final_prompt, GEMINI_API_KEY, gemini_q, gemini_done, gemini_result),
#             daemon=True
#         ).start()

#         threading.Thread(
#             target=run_gpt,
#             args=(temp_path, final_prompt, OPENAI_API_KEY, gpt_result, gpt_done),
#             daemon=True
#         ).start()

#         # Polling + Output mgmt
#         first_shown = None
#         gemini_output = ""

#         gemini_start = time.time()
#         gpt_start = time.time()

#         while not (gemini_done.is_set() and gpt_done.is_set()):

#             # Update timers
#             gemini_timer.write(f"Gemini Time: {time.time() - gemini_start:.1f}s")
#             gpt_timer.write(f"GPT-5 Time: {time.time() - gpt_start:.1f}s")

#             # Handle Gemini streaming
#             try:
#                 chunk = gemini_q.get_nowait()
#                 if chunk is None:
#                     pass
#                 else:
#                     gemini_output += chunk

#                     if first_shown is None:
#                         first_shown = "gemini"
#                         first_title.markdown("### 🟦 First Finished (Streaming): Gemini")
#                     first_output.markdown(gemini_output)

#             except queue.Empty:
#                 pass

#             # If GPT finishes first
#             if gpt_done.is_set() and first_shown is None:
#                 first_shown = "gpt"
#                 first_title.markdown("### 🟥 First Finished: GPT-5")
#                 first_output.write(gpt_result["text"])

#             # If Gemini first, GPT second
#             if gpt_done.is_set() and first_shown == "gemini":
#                 second_title.markdown("### 🟥 Second (GPT-5)")
#                 second_output.write(gpt_result["text"])

#             # If GPT first, Gemini second
#             if gemini_done.is_set() and first_shown == "gpt":
#                 second_title.markdown("### 🟦 Second (Gemini)")
#                 second_output.write(gemini_output)

#             time.sleep(0.05)

#         status_box.success("🎉 Both models completed!")


# pages/file.py
import streamlit as st
import yaml
import time
import threading
import queue
import os
import re
from google import genai
from google.genai import types
from openai import OpenAI

st.title("📄 PDF Case Study Generator")
if st.button("⬅ Back to Mode Selection"):
    st.switch_page("app.py")  # go to root (app)

# Model selection radio
model_choice = st.radio("Select Model", ["GPT-5 Only", "Gemini Only", "Both"], index=2)

# Show API key inputs depending on selection
OPENAI_API_KEY = ""
GEMINI_API_KEY = ""

if model_choice in ("GPT-5 Only", "Both"):
    OPENAI_API_KEY = st.text_input("OpenAI API Key (GPT-5)", type="password")
if model_choice in ("Gemini Only", "Both"):
    GEMINI_API_KEY = st.text_input("Gemini API Key", type="password")

st.divider()

# load YAML template safely
prompt_template = None
try:
    with open("prompts.yaml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    prompt_template = data.get("case_study_maths")
    if not prompt_template:
        st.error("prompts.yaml is missing the 'case_study_maths' template.")
except FileNotFoundError:
    st.error("prompts.yaml not found in working directory. Prompt preview disabled.")
except Exception as e:
    st.error(f"Error loading prompts.yaml: {e}")

# PDF uploader and inputs
uploaded_pdf = st.file_uploader("Upload PDF (required for PDF mode)", type=["pdf"])
st.subheader("Case Study Configuration (from PDF mode)")
grade = st.number_input("Grade", 1, 12, 10)
curriculum = st.text_input("Curriculum", "NCERT")
subject = st.text_input("Subject", "Maths")
chapter = st.text_input("Chapter / Unit", "Surface area and volume")
topic = st.text_input("Topic(s)", "Volume of a Combination of Solids")
num_questions = st.number_input("Number of Questions", 1, 20, 2)
num_subparts = st.number_input("Number of Subparts", 1, 6, 3)

st.subheader("Old Concept + Additional Notes")
old_concepts = st.text_area("Old Concept", "Surface area, Volume, Shapes etc.")
additional_note = st.text_area("Additional Note for Solution", "Ensure steps are clear and units are consistent.")

# Subparts config
dok_levels = []
marks_per_subpart = []
for i in range(num_subparts):
    label = chr(97 + i)
    c1, c2 = st.columns(2)
    with c1:
        dok = st.selectbox(f"DOK ({label})", ["DOK 1", "DOK 2", "DOK 3"], key=f"dok_f_{i}")
    with c2:
        marks = st.number_input(f"Marks ({label})", 1, 10, 1, key=f"marks_f_{i}")
    dok_levels.append(dok)
    marks_per_subpart.append(marks)

subparts_block = "\n".join([
    f"  - Part ({chr(97+i)}): [{marks_per_subpart[i]} Mark(s), {dok_levels[i]}]"
    for i in range(num_subparts)
])

# Build prompt (safe replacement using regex)
def build_prompt(template, mapping, subparts_text, extra_text):
    if not template:
        return None
    out = template
    # replace placeholders like {{Key}} ignoring whitespace
    for k, v in mapping.items():
        pattern = re.compile(r"\{\{\s*" + re.escape(k) + r"\s*\}\}", re.IGNORECASE)
        out = pattern.sub(str(v), out)
    out = out.replace("{{SUBPARTS_SECTION}}", subparts_text)
    out = out + "\n\n" + extra_text
    return out

input_data = {
    "Grade": grade,
    "Curriculam": curriculum,
    "Subject": subject,
    "Topic": topic,
    "Number_of_questions": num_questions,
    "Number_of_subparts": num_subparts,
    "Chapter": chapter,
}

extra_text = f"Old concept: {old_concepts}\n\nAlso follow this additional instruction strictly while generating the solution:\n{additional_note}"

final_prompt = build_prompt(prompt_template, input_data, subparts_block, extra_text)

# if final_prompt:
#     with st.expander("Preview final prompt"):
#         st.code(final_prompt[:10000])  # show only first 10k chars to avoid UI freeze

# Output placeholders (conditionally shown)
if model_choice in ("Both", "Gemini Only"):
    gemini_timer = st.empty()
    gemini_output_area = st.empty()
if model_choice in ("Both", "GPT-5 Only"):
    gpt_timer = st.empty()
    gpt_output_area = st.empty()

status_box = st.empty()

# Threading helpers
def run_gemini_stream(pdf_bytes, prompt, api_key, q, done_flag, result_store):
    start = time.time()
    try:
        client = genai.Client(api_key=api_key)
        pdf_part = types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf")
        config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(include_thoughts=False, thinking_budget=3000)
        )
        stream = client.models.generate_content_stream(
            model="gemini-2.5-pro",
            contents=[pdf_part, prompt],
            config=config
        )
        for chunk in stream:
            text_chunk = getattr(chunk, "text", "") or ""
            if text_chunk:
                q.put(text_chunk)
    except Exception as e:
        q.put(f"[Gemini Error] {e}")
    finally:
        q.put(None)
        result_store["elapsed"] = time.time() - start
        done_flag.set()

def run_gpt(pdf_path, prompt, api_key, result_store, done_flag):
    start = time.time()
    try:
        client = OpenAI(api_key=api_key)
        fobj = open(pdf_path, "rb")
        uploaded = client.files.create(file=fobj, purpose="user_data")
        fobj.close()
        response = client.responses.create(
            model="gpt-5",
            input=[
                {"role": "user",
                 "content": [
                     {"type": "input_file", "file_id": uploaded.id},
                     {"type": "input_text", "text": prompt},
                 ]}
            ]
        )
        # safe extraction
        text = getattr(response, "output_text", None)
        if text is None:
            try:
                text = response.output[0].content[0].text
            except Exception:
                text = str(response)
        result_store["text"] = text
        # delete uploaded file
        try:
            client.files.delete(uploaded.id)
        except Exception:
            pass
    except Exception as e:
        result_store["text"] = f"[GPT-5 Error] {e}"
    finally:
        result_store["elapsed"] = time.time() - start
        done_flag.set()

# Run button
if st.button("🚀 Run Selected Model(s)"):
    # Basic validation
    if model_choice in ("Both", "GPT-5 Only") and (not OPENAI_API_KEY):
        st.error("OpenAI API key required for GPT-5")
    elif model_choice in ("Both", "Gemini Only") and (not GEMINI_API_KEY):
        st.error("Gemini API key required for Gemini")
    elif model_choice in ("Both", "Gemini Only") and (uploaded_pdf is None):
        st.error("Please upload a PDF for Gemini to consume.")
    else:
        # Prepare shared structures
        gemini_enabled = model_choice in ("Both", "Gemini Only")
        gpt_enabled = model_choice in ("Both", "GPT-5 Only")
        gemini_q = queue.Queue()
        gemini_done = threading.Event()
        gpt_done = threading.Event()
        gemini_result = {"text": "", "elapsed": None}
        gpt_result = {"text": "", "elapsed": None}

        temp_pdf_path = None
        if uploaded_pdf is not None:
            pdf_bytes = uploaded_pdf.read()
            temp_pdf_path = "temp_file_uploaded.pdf"
            with open(temp_pdf_path, "wb") as f:
                f.write(pdf_bytes)

        # Start threads conditionally
        if gemini_enabled:
            threading.Thread(
                target=run_gemini_stream,
                args=(pdf_bytes, final_prompt, GEMINI_API_KEY, gemini_q, gemini_done, gemini_result),
                daemon=True
            ).start()

        if gpt_enabled:
            # GPT needs a file path (we provided temp_pdf_path)
            threading.Thread(
                target=run_gpt,
                args=(temp_pdf_path, final_prompt, OPENAI_API_KEY, gpt_result, gpt_done),
                daemon=True
            ).start()

        status_box.info("Generation started...")

        # Polling loop (works for single or both)
        gemini_agg = ""
        first_shown = None
        gemini_start = time.time()
        gpt_start = time.time()

        while True:
            # timers
            if gemini_enabled:
                gemini_timer.write(f"Gemini Time: {time.time()-gemini_start:.1f}s")
            if gpt_enabled:
                gpt_timer.write(f"GPT-5 Time: {time.time()-gpt_start:.1f}s")

            # handle gemini stream
            if gemini_enabled:
                try:
                    chunk = gemini_q.get_nowait()
                    if chunk is None:
                        pass
                    else:
                        gemini_agg += chunk
                        if first_shown is None:
                            first_shown = "gemini"
                            gemini_output_area.markdown("### 🟦 Gemini (streaming) — first output", unsafe_allow_html=True)
                        # show streaming or final depending on mode
                        gemini_output_area.markdown(gemini_agg, unsafe_allow_html=True)
                except queue.Empty:
                    pass

            # if GPT finished
            if gpt_enabled and gpt_done.is_set() and gpt_result.get("text") is not None and first_shown is None:
                first_shown = "gpt"
                gpt_output_area.markdown("### 🟥 GPT-5 — first output")
                gpt_output_area.text(gpt_result["text"])

            # when both finished or single finished -> break
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
                # show gemini in second area or alone
                gemini_output_area.markdown("### 🟦 Gemini (final)")
                gemini_output_area.markdown(gemini_result["text"], unsafe_allow_html=True)
        if gpt_enabled:
            gpt_timer.write(f"GPT-5 Time: {gpt_result['elapsed']:.2f}s")
            if first_shown != "gpt":
                gpt_output_area.markdown("### 🟥 GPT-5")
                gpt_output_area.text(gpt_result["text"])

        status_box.success("🎉 Completed")
        # cleanup temp file
        if temp_pdf_path and os.path.exists(temp_pdf_path):
            try:
                os.remove(temp_pdf_path)
            except Exception:
                pass
