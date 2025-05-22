import streamlit as st
import json

# Load config
with open("quiz_config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

st.set_page_config(page_title="Business Scan", layout="wide")

# Collect responses
responses = {}

# Iterate over pages
for page in config["pages"]:
    st.header(page["title"])
    for q in page["questions"]:
        qid = q["id"]
        label = q["label"]

        if q["type"] == "select":
            responses[qid] = st.selectbox(label, q["options"])
        elif q["type"] == "radio":
            responses[qid] = st.radio(label, q["options"])
        elif q["type"] == "slider":
            # Professional: show text labels directly in the slider
            responses[qid] = st.select_slider(label, options=q["labels"])
        elif q["type"] == "text":
            responses[qid] = st.text_input(label)
        elif q["type"] == "email":
            responses[qid] = st.text_input(label, type="email")
        elif q["type"] == "checkbox":
            responses[qid] = st.checkbox(label)

    st.markdown("---")

# Submit button and output
if st.button("Verzenden"):
    st.success("Bedankt voor je antwoorden!")
    st.json(responses)
