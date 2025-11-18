# import streamlit as st

# # Hide multipage menu
# st.markdown("""
# <style>
# section[data-testid="stSidebar"] ul {display: none !important;}
# </style>
# """, unsafe_allow_html=True)

# st.title("📘 NCERT Case Study Generator")
# st.write("Select an input mode to continue:")

# mode = st.radio(
#     "Choose Input Mode",
#     ["-- Select Mode --", "Manual Input", "PDF Upload"],
#     index=0
# )

# if mode == "Manual Input":
#     st.switch_page(r"pages/o.py")

# elif mode == "PDF Upload":
#     st.switch_page(r"pages/file.py")


import streamlit as st

# Hide sidebar
st.set_page_config(page_title="NCERT Case Study Generator", layout="centered")
st.markdown("""
<style>
section[data-testid="stSidebar"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

st.title("📘 NCERT Case Study Generator")
st.write("Select an input mode to continue:")

mode = st.radio(
    "Choose Input Mode",
    ["-- Select Mode --", "Manual Input", "PDF Upload"],
    index=0
)

st.write("")
if st.button("Continue"):
    if mode == "Manual Input":
        st.switch_page("pages/o.py")
    elif mode == "PDF Upload":
        st.switch_page("pages/file.py")
    else:
        st.warning("Please choose a valid mode first.")
