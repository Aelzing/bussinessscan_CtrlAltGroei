import streamlit as st
import json

# 1. Config laden
with open("quiz_config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# 2. Door pagina's loopen
responses = {}
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
            responses[qid] = st.slider(label,
                                       min_value=q["min"],
                                       max_value=q["max"],
                                       step=q["step"],
                                       format="%d")
        elif q["type"] == "text":
            responses[qid] = st.text_input(label)
        elif q["type"] == "email":
            responses[qid] = st.text_input(label, type="email")
        elif q["type"] == "checkbox":
            responses[qid] = st.checkbox(label)
    st.write("---")

# 3. Verwerken of rapport tonen
if st.button("Verzenden"):
    st.write("Bedankt voor je antwoorden!")
    st.json(responses)
