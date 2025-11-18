
# # app.py
# import streamlit as st
# import yaml
# import time
# import threading
# import queue
# from google import genai
# from google.genai import types # Important: Need to import types for configuration objects


# from openai import OpenAI         # GPT-5 client (keeps your original usage)
# from google import genai         # Gemini client

# # ----------------------------
# # API KEYS (replace these)
# # ----------------------------
# import streamlit as st

# if st.button("⬅ Back to Mode Selection"):
#     st.switch_page("app.py")

# st.title("📝 Manual Case Study Generator")

# # ... your full manual code ...

# st.markdown("### 🔐 API Keys")

# OPENAI_API_KEY = st.text_input("OpenAI API Key (for GPT-5)", type="password")
# GEMINI_API_KEY = st.text_input("Gemini API Key", type="password")

# if not OPENAI_API_KEY or not GEMINI_API_KEY:
#     st.warning("Please enter both API keys to continue.")

# # ----------------------------
# # Load prompt template
# # ----------------------------
# with open("prompts.yaml", "r", encoding="utf-8") as file:
#     data = yaml.safe_load(file)
# prompt_template = data["case_study_maths"]

# # ----------------------------
# # Streamlit UI - Inputs
# # ----------------------------
# st.title("📘 Simple NCERT Case Study Generator")

# st.info("PDF upload removed — Manual Input only.")

# # Inputs (kept same as your original UI)
# grade = st.number_input("Grade", 1, 12, 10)
# curriculum = st.text_input("Curriculum", "NCERT")
# subject = st.selectbox("Subject", ["Maths"])
# num_questions = st.number_input("Number of Case-Based Questions", 1, 20, 2)

# st.markdown("### Subpart Configuration")
# num_subparts = st.number_input("Number of Subparts", 1, 6, 3)

# dok_levels = []
# marks_per_subpart = []
# for i in range(num_subparts):
#     label = chr(97 + i)
#     col1, col2 = st.columns(2)
#     with col1:
#         dok = st.selectbox(f"DOK Level ({label})", ["DOK 1", "DOK 2", "DOK 3"], key=f"dok_{i}")
#     with col2:
#         marks = st.number_input(f"Marks ({label})", 1, 10, 1, key=f"marks_{i}")
#     dok_levels.append(dok)
#     marks_per_subpart.append(marks)

# subparts_block = "\n".join([
#     f"  - Part ({chr(97 + i)}): [{marks_per_subpart[i]} Mark(s), {dok_levels[i]}]"
#     for i in range(num_subparts)
# ])

# chapter = st.text_input("Chapter / Unit", "Surface area and volume")
# topic = st.text_input("Topic(s)", "Volume of a Combination of Solids")
# concepts = st.text_area("Key Concepts", "Surface area, Volume, Shapes conversion etc.")

# # Build final prompt
# input_data = {
#     "Grade": grade,
#     "Curriculam": curriculum,
#     "Subject": subject,
#     "Topic": topic,
#     "Number_of_questions": num_questions,
#     "Number_of_subparts": num_subparts,
#     "Chapter": chapter,
#     "Concepts": concepts,
# }

# prompt_filled = prompt_template
# for key, value in input_data.items():
#     prompt_filled = prompt_filled.replace(f"{{{{{key}}}}}", str(value))
# prompt_filled = prompt_filled.replace("{{SUBPARTS_SECTION}}", subparts_block)
# final_prompt = prompt_filled

# st.markdown("---")

# # Placeholders and status areas
# controls_col, timers_col = st.columns([3, 2])

# with controls_col:
#     generate_btn = st.button("🚀 Generate Case Study")

# with timers_col:
#     gemini_timer_placeholder = st.empty()
#     gpt_timer_placeholder = st.empty()
#     overall_status = st.empty()

# # Output placeholders (vertical layout: top = first finished, bottom = second)
# top_output_box = st.container()      # will contain whichever finishes first (stream or final)
# st.markdown("### Outputs (first finished shown above; second shown below)")
# first_output_title = st.empty()
# first_output_area = st.empty()
# second_output_title = st.empty()
# second_output_area = st.empty()

# # Internal shared state
# gemini_queue = queue.Queue()
# gemini_done = threading.Event()
# gpt_done = threading.Event()
# gpt_result = {"text": None, "elapsed": None}
# gemini_result = {"text": "", "elapsed": None}
# first_shown = {"set": False, "which": None}  # 'gemini' or 'gpt'

# def run_gemini_stream(prompt, api_key, q: queue.Queue, done_event: threading.Event, result_store: dict):
#     """
#     Calls Gemini streaming API and puts chunks into queue.
#     On completion puts a sentinel (None).
#     Records elapsed time into result_store["elapsed"].
#     """
#     client = genai.Client(api_key=api_key)
#     start = time.time()
#     try:
        
#         # 1. Define the configuration objects
#         thinking_config = types.ThinkingConfig(
#             # output_thinking=True is not necessary if you use thinkingBudget > 0 or -1,
#             # but include_thoughts=True is needed to stream the *text* of the thoughts.
#             # The documentation suggests using 'include_thoughts=True' to view thought summaries.
#             include_thoughts=True,     
            
#             # For 2.5 Pro, thinking is on by default.
#             # We set a manual budget of 5000 tokens here.
#             # Range for 2.5 Pro is 128 to 32768. Use -1 for Dynamic/Auto.
#             thinking_budget=10000       
#         )

#         config = types.GenerateContentConfig(
#             thinking_config=thinking_config
#         )

#         try:
#             # generate_content_stream yields incremental chunks
#             response = client.models.generate_content_stream(
#                 model="gemini-2.5-pro",
#                 contents=[prompt],
#                 config=config # <--- This is the correct parameter name!
#             )
            
#             # iterate stream
#             for chunk in response:
#                 # chunk may have .text (or similar) — use .text per example
#                 text_chunk = getattr(chunk, "text", "") or ""
#                 if text_chunk:
#                     q.put(text_chunk)
                    
#             # stream finished
#         except Exception as e:
#             print(f"An error occurred: {e}")
#         # # iterate stream
#         # for chunk in response:
#         #     # chunk may have .text (or similar) — use .text per example
#         #     text_chunk = getattr(chunk, "text", "") or ""
#         #     if text_chunk:
#         #         q.put(text_chunk)
        
#         # stream finished
#     except Exception as e:
#         q.put(f"\n\n[Gemini stream error] {e}\n")
#     finally:
#         elapsed = time.time() - start
#         result_store["elapsed"] = elapsed
#         done_event.set()
#         q.put(None)  # sentinel to indicate completion

# def run_gpt_nonstream(prompt, api_key, result_store: dict, done_event: threading.Event):
#     """
#     Calls OpenAI Responses (GPT-5) synchronously (non-streaming).
#     Stores result text and elapsed time in result_store and sets done_event.
#     """
#     client = OpenAI(api_key=api_key)
#     start = time.time()
#     try:
#         response = client.responses.create(
#             model="gpt-5",
#             reasoning={"effort": "medium"},
#             input=prompt
#         )
#         # Keep same field as your original code (output_text)
#         text = getattr(response, "output_text", None)
#         if text is None:
#             # fallback: some SDKs return .output[0].content[0].text or similar
#             # try a conservative fallback (not guaranteed)
#             try:
#                 text = response.output[0].content[0].text
#             except Exception:
#                 text = str(response)
#         result_store["text"] = text
#     except Exception as e:
#         result_store["text"] = f"[GPT-5 error] {e}"
#     finally:
#         result_store["elapsed"] = time.time() - start
#         done_event.set()

# # This function manages UI updates while background threads run
# def orchestrate_generation():
#     # reset states
#     while not gemini_queue.empty():
#         try:
#             gemini_queue.get_nowait()
#         except queue.Empty:
#             break
#     gemini_done.clear()
#     gpt_done.clear()
#     first_shown["set"] = False
#     first_shown["which"] = None
#     gpt_result["text"] = None
#     gpt_result["elapsed"] = None
#     gemini_result["text"] = ""
#     gemini_result["elapsed"] = None

#     # placeholders initial
#     gemini_timer_placeholder.write("Gemini Time: 0.0s")
#     gpt_timer_placeholder.write("GPT-5 Time: 0.0s")
#     overall_status.info("Started generation...")

#     # start time trackers
#     start_time = time.time()
#     gemini_start = time.time()
#     gpt_start = time.time()

#     # start background threads
#     gemini_thread = threading.Thread(
#         target=run_gemini_stream,
#         args=(final_prompt, GEMINI_API_KEY, gemini_queue, gemini_done, gemini_result),
#         daemon=True
#     )
#     gpt_thread = threading.Thread(
#         target=run_gpt_nonstream,
#         args=(final_prompt, OPENAI_API_KEY, gpt_result, gpt_done),
#         daemon=True
#     )

#     gemini_thread.start()
#     gpt_thread.start()

#     # We'll aggregate gemini text as it arrives
#     aggregated_gemini_text = ""
#     gemini_first_chunk_received = False

#     # main polling loop: runs until both done
#     while not (gpt_done.is_set() and gemini_done.is_set()):
#         # update timers
#         now = time.time()
#         gemini_elapsed = (now - gemini_start)
#         gpt_elapsed = (now - gpt_start)
#         gemini_timer_placeholder.write(f"Gemini Time: {gemini_elapsed:.1f}s")
#         gpt_timer_placeholder.write(f"GPT-5 Time: {gpt_elapsed:.1f}s")

#         # process any gemini chunks
#         try:
#             # non-blocking get
#             chunk = gemini_queue.get(timeout=0.1)
#             if chunk is None:
#                 # sentinel => gemini finished
#                 pass
#             else:
#                 gemini_first_chunk_received = True
#                 aggregated_gemini_text += chunk
#                 gemini_result["text"] = aggregated_gemini_text  # keep updating
#                 # If nothing shown yet (first result), and GPT hasn't finished showing first => show gemini streaming as first
#                 if not first_shown["set"]:
#                     first_shown["set"] = True
#                     first_shown["which"] = "gemini"
#                     first_output_title.markdown("**First finished (streaming): Gemini**")

#                     # show streaming area (will update on next chunks)
#                     first_output_area.markdown(aggregated_gemini_text, unsafe_allow_html=True)
#                     st.markdown("<hr style='border:1px solid #555; margin:15px 0;'>", unsafe_allow_html=True)

#                     # reserve area for GPT below - will fill later
#                     second_output_title.markdown("**Second (GPT-5)**")
#                     second_output_area.info("Waiting for GPT-5...")
#                 else:
#                     # If Gemini is first shown, update the streaming text area
#                     if first_shown["which"] == "gemini":
#                         first_output_area.markdown(aggregated_gemini_text, unsafe_allow_html=True)

#                     else:
#                         # First shown is GPT -> update second area (gemini streaming)
#                         second_output_area.markdown(aggregated_gemini_text, unsafe_allow_html=True)

#         except queue.Empty:
#             # no chunk available; ok
#             pass

#         # If GPT finished and it's not yet displayed as first (and gemini hasn't streamed yet),
#         # display GPT immediately as first result.
#         if gpt_done.is_set() and not first_shown["set"]:
#             first_shown["set"] = True
#             first_shown["which"] = "gpt"
#             first_output_title.markdown("**First finished: GPT-5**")
#             first_output_area.text(gpt_result["text"])
#             st.markdown("<hr style='border:1px solid #555; margin:15px 0;'>", unsafe_allow_html=True)
#             # reserve second area for Gemini
#             second_output_title.markdown("**Second (Gemini streaming)**")
#             second_output_area.info("Waiting for Gemini stream...")
#         # If GPT finished after Gemini was first, place GPT in second area
#         if gpt_done.is_set() and first_shown["set"] and first_shown["which"] == "gemini":
#             # only update second area once
#             if second_output_area is not None and (gpt_result["text"] is not None):
#                 # show GPT result below
#                 second_output_area.text(gpt_result["text"])

#         # small sleep so UI updates are visible and loop isn't busy
#         time.sleep(0.05)

#     # final updates once both done
#     # gemini_result["elapsed"] already set by gemini thread; gpt_result too
#     gemini_timer_placeholder.write(f"Gemini Time: {gemini_result['elapsed']:.2f}s")
#     gpt_timer_placeholder.write(f"GPT-5 Time: {gpt_result['elapsed']:.2f}s")

#     # Ensure final texts are shown in the correct slots:
#     if first_shown["which"] == "gemini":
#         # first area already contains gemini final text
#         first_output_area.markdown(gemini_result["text"], unsafe_allow_html=True)

#         second_output_title.markdown("**Second (GPT-5)**")
#         second_output_area.text(gpt_result["text"])
#     elif first_shown["which"] == "gpt":
#         first_output_area.text(gpt_result["text"])
#         second_output_title.markdown("**Second (Gemini)**")
#         second_output_area.text(gemini_result["text"])
#     else:
#         # fallback: nothing was shown first (rare) -> show both
#         first_output_title.markdown("**GPT-5**")
#         first_output_area.text(gpt_result["text"])
#         second_output_title.markdown("**Gemini**")
#         second_output_area.text(gemini_result["text"])

#     overall_status.success("Both models finished.")
#     st.write("---")
#     st.markdown(f"**Final times:** GPT-5 = {gpt_result['elapsed']:.2f}s  |  Gemini = {gemini_result['elapsed']:.2f}s")
#     st.balloons()

# # Trigger generation
# if generate_btn:
#     # Basic UI validation for keys
#     if OPENAI_API_KEY.startswith("YOUR") or GEMINI_API_KEY.startswith("YOUR"):
#         st.error("Please replace OPENAI_API_KEY and GEMINI_API_KEY with real keys in the script.")
#     else:
#         # Run orchestrator in main thread (it starts background threads and polls)
#         orchestrate_generation()


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
