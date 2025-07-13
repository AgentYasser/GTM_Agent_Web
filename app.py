import streamlit as st
import json
import os

# OpenAI import
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

# Core functions
from agent_core import get_gtm_variable_details

# Load JSON data
def load_json(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}

gtm_data = load_json('structured_gtm_variables.json')
config   = load_json('director_config.json')
runtime  = load_json('gtm_runtime_data.json')

# Page setup
st.set_page_config(page_title="GTM AI Agent - Chat First", layout="centered")
st.title("📊 GTM AI Agent")

# Chat-first UI
st.header("💬 Chat with GTM Agent")
prompt = st.text_area("Ask anything about GTM:", height=150)
if st.button("Send to AI"):
    if not openai.api_key:
        st.error("OPENAI_API_KEY not set. Please add it in Streamlit Secrets.")
    else:
        with st.spinner("Thinking..."):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": (
                        "You are a GTM AI assistant. Here are the GTM variables and their purposes:" +
                        json.dumps(gtm_data, indent=2)
                    )},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
        answer = response.choices[0].message.content
        st.markdown("**AI Answer:**")
        st.write(answer)

st.markdown("---")
# Tier-based Query below
st.header("🔍 Query by Tier & Variable")
tier = st.selectbox("Select Tier", list(gtm_data.keys()))
variable = st.selectbox("Select Variable", list(gtm_data.get(tier, {})))
if st.button("Get Recommendation"):
    res = get_gtm_variable_details(gtm_data, config, runtime, tier, variable)
    st.json(res)

st.sidebar.info("Use the chat above or query by selecting a tier and variable.")
