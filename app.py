import streamlit as st
import json
import os

from transformers import pipeline, Conversation

# ———— Load GTM Data ————
@st.cache_data
def load_json(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}

gtm_data = load_json("structured_gtm_variables.json")
tiers = list(gtm_data.keys())

# ———— Sidebar: Tier & Variable Selection ————
st.sidebar.header("GTM AI Agent")
selected_tier = st.sidebar.selectbox("Select Tier", tiers)
vars_in_tier = list(gtm_data.get(selected_tier, {}).keys())
selected_var = st.sidebar.selectbox("Select Variable", vars_in_tier)

if st.sidebar.button("Show Definition"):
    info = gtm_data[selected_tier][selected_var]
    st.sidebar.markdown(f"**Purpose:** {info['Purpose']}")
    st.sidebar.markdown(f"**Inputs:** {info['Inputs']}")
    st.sidebar.markdown(f"**Example:** {info['Example']}")

# ———— Initialize Chat Model ————
@st.cache_resource(show_spinner=False)
def get_chatbot():
    return pipeline(
        "conversational",
        model="microsoft/DialoGPT-medium",
        device=-1
    )

chatbot = get_chatbot()

# ———— Main Area: Chat Interface ————
st.title("💬 GTM AI Agent")
user_query = st.text_input("Ask anything about GTM…")

if st.button("Send to AI") and user_query:
    conv = Conversation(user_query)
    conv = chatbot(conv)
    reply = conv.generated_responses[-1]
    st.markdown(f"**AI Answer:** {reply}")

# ———— Show Current Runtime Value ————
runtime = load_json("gtm_runtime_data.json")
current_val = runtime.get(selected_tier, {}).get(selected_var, "No data")
st.info(f"Current value for **{selected_var}**: {current_val}")
