import streamlit as st
import json
import requests

# 1) Zet hier je echte n8n-webhook-URL
WEBHOOK_URL = "https://ctrlaltgroei.app.n8n.cloud/webhook/businessscan"
CONFIG_PATH = "quiz_config.json"

# 2) Laad de vragenlijst-config
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

st.set_page_config(page_title="Business Scan", layout="wide")
st.title("Business Scan")

# 3) Verzamel de antwoorden
responses = {}
for page in config["pages"]:
    st.header(page["title"])
    for q in page["questions"]:
        qid = q["id"]
        label = q["label"]

        if q["type"] == "select":
            responses[qid] = st.selectbox(label, q["options"], key=qid)
        elif q["type"] == "radio":
            responses[qid] = st.radio(label, q["options"], key=qid)
        elif q["type"] == "slider":
            responses[qid] = st.select_slider(label, options=q["labels"], key=qid)
        elif q["type"] == "text":
            responses[qid] = st.text_input(label, key=qid)
        elif q["type"] == "email":
            responses[qid] = st.text_input(label, key=qid)
        elif q["type"] == "checkbox":
            responses[qid] = st.checkbox(label, key=qid)

    st.markdown("---")

# 4) Knop: valideer e-mail en stuur POST
if st.button("Verzenden"):
    # Vind e-mail uit responses
    email = responses.get("email", "").strip()
    # Eenvoudige validatie
    if not email or "@" not in email:
        st.error("Vul eerst een geldig e-mailadres in voordat je verzendt.")
    else:
        # Verstuur naar n8n
        try:
            resp = requests.post(WEBHOOK_URL, json={"responses": responses})
            resp.raise_for_status()
            st.success("Je antwoorden zijn succesvol verzonden! 🎉")
        except Exception as e:
            st.error(f"Fout bij verzenden naar webhook: {e}")
