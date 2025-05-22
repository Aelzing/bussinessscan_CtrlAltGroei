import streamlit as st
import json
from email_validator import validate_email, EmailNotValidError

# Load config
with open("quiz_config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

st.set_page_config(page_title="Business Scan", layout="wide")
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
            responses[qid] = st.select_slider(label, options=q["labels"])

        elif q["type"] == "text":
            responses[qid] = st.text_input(label)

        elif q["type"] == "email":
            email_input = st.text_input(label)
            try:
                valid = validate_email(email_input)
                responses[qid] = valid.email
            except EmailNotValidError:
                st.error("Ongeldig e-mailadres")
                responses[qid] = None

        elif q["type"] == "checkbox":
            responses[qid] = st.checkbox(label)

    # Scheiding tussen pagina’s
    st.markdown("---")

import requests

if st.button("Verzenden"):
    # validatie e-mail zoals voorheen
    if not email:
        st.error("Vul eerst een geldig e-mailadres in.")
    else:
        payload = {"responses": responses}
        # Roep je n8n-webhook aan
        resp = requests.post("https://ctrlaltgroei.app.n8n.cloud/webhook/businessscan", json={"responses": responses})

        if resp.ok:
            st.success("Bedankt! Je ontvangt zo snel mogelijk een persoonlijk advies per mail.")
        else:
            st.error("Er ging iets mis bij het versturen van je antwoorden.")

