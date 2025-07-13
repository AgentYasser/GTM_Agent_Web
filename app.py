import streamlit as st
import json
import os

# Try import OpenAI
try:
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")
    HAS_OPENAI = True
except:
    HAS_OPENAI = False

# Core functions
from agent_core import get_gtm_variable_details

# Load data
def load_json(path):
    if os.path.exists(path):
        return json.load(open(path))
    return {}

gtm_data = load_json('structured_gtm_variables.json')
config   = load_json('director_config.json')
runtime  = load_json('gtm_runtime_data.json')

# Page config & title
st.set_page_config(page_title="GTM AI Agent - Chat First", layout="centered")
st.title("📊 GTM AI Agent")

# Chat-first UI
st.header("💬 Chat with GTM Agent")
prompt = st.text_area("Ask anything about GTM:", height=150)
if prompt:
    if st.button("Send to AI"):
        if not HAS_OPENAI:
            st.error("OpenAI SDK unavailable or API key missing.")
        else:
            context = "You are a GTM AI assistant. Here are GTM variables:\n" + json.dumps(gtm_data, indent=2)
            resp = openai.Completion.create(
                engine="text-davinci-003",
                prompt=context + "\nUser: " + prompt,
                max_tokens=300,
                temperature=0.7
            )
            st.markdown("**AI Answer:**")
            st.write(resp.choices[0].text.strip())

st.markdown("---")
# Tier-based Query below
st.header("🔍 Query by Tier & Variable")
tier = st.selectbox("Select Tier", list(gtm_data.keys()))
variable = st.selectbox("Select Variable", list(gtm_data.get(tier, {})))
if st.button("Get Recommendation"):
    res = get_gtm_variable_details(gtm_data, config, runtime, tier, variable)
    st.json(res)

st.sidebar.info("Use the chat above or query by selecting a tier and variable.")
