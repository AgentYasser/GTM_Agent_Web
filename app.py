import streamlit as st
import json
import os
import csv
import datetime
import matplotlib.pyplot as plt

from agent_core import (
    personalize_output,
    smart_recommendation,
    performance_feedback,
    get_gtm_variable_details
)

# Load data
GTM_PATH = "structured_gtm_variables.json"
CONFIG_PATH = "director_config.json"
RUNTIME_PATH = "gtm_runtime_data.json"

gtm_data = json.load(open(GTM_PATH))
config = json.load(open(CONFIG_PATH))
runtime_raw = json.load(open(RUNTIME_PATH)) if os.path.exists(RUNTIME_PATH) else {}

# Map raw sheet keys to tier names
mapping = {
    'Tier1A_Empower': 'Tier_1A_Individual_Empowerment',
    'Tier1B_Behavior': 'Tier_1B_Behavioral_Calibration',
    'Tier2_InsightOpt': 'Tier_2_Director_Insight_Optimization',
    'Tier3_Systemic': 'Tier_3_Systemic_Integration'
}
runtime = {mapping.get(k, k): v for k, v in runtime_raw.items()}

st.set_page_config(page_title="GTM AI Agent", layout="wide")
st.title("📊 GTM AI Agent")
st.sidebar.header("Navigation")

mode = st.sidebar.selectbox("Choose action", [
    "Query Variable", "Update Value", "Batch Report", 
    "Trend Dashboard", "Natural-Language Query"
])

if mode == "Query Variable":
    tier = st.selectbox("Select Tier", list(gtm_data.keys()))
    variable = st.selectbox("Select Variable", list(gtm_data[tier].keys()))
    if st.button("Get Recommendation"):
        result = get_gtm_variable_details(gtm_data, config, runtime, tier, variable)
        st.subheader("🔍 Recommendation")
        for k, v in result.items():
            st.write(f"**{k}:** {v}")

elif mode == "Update Value":
    tier = st.selectbox("Select Tier", list(runtime.keys()))
    variable = st.selectbox("Select Variable", list(runtime.get(tier, {}).keys()))
    new_val = st.text_input("New Value", value=runtime.get(tier, {}).get(variable, ""))
    if st.button("Update"):
        runtime.setdefault(tier, {})[variable] = new_val
        with open(RUNTIME_PATH, 'w') as f:
            json.dump(runtime_raw, f, indent=4)
        st.success("Value updated.")

elif mode == "Batch Report":
    if st.button("Generate CSV Report"):
        rows = []
        for t, vars in gtm_data.items():
            for v in vars:
                rec = get_gtm_variable_details(gtm_data, config, runtime, t, v)
                rows.append({
                    "Tier": t,
                    "Variable": v,
                    "Purpose": rec['Personalized Purpose'],
                    "Value": rec['Current Value']
                })
        df = st.dataframe(rows)
        csv_data = df.to_csv(index=False)
        st.download_button("Download Report", data=csv_data, file_name="GTM_Report.csv")

elif mode == "Trend Dashboard":
    if os.path.exists('trend_log.csv'):
        timestamps, values = [], []
        with open('trend_log.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                timestamps.append(datetime.datetime.fromisoformat(row['Timestamp']))
                values.append(float(row['Value']))
        st.line_chart({"Values": values}, x=timestamps)
    else:
        st.info("No trend data logged yet.")

elif mode == "Natural-Language Query":
    query = st.text_input("Ask your GTM question...")
    if st.button("Map & Query"):
        keywords = {
            'pipeline': 'Trend_Synthesizer',
            'insight': 'Insight_Generator',
            'alignment': 'Alignment_Tracker'
        }
        var = next((v for k, v in keywords.items() if k in query.lower()), None)
        if var:
            tier = next(t for t, vars in gtm_data.items() if var in vars)
            result = get_gtm_variable_details(gtm_data, config, runtime, tier, var)
            st.write(f"**Mapped to:** {tier} → {var}")
            for k, v in result.items():
                st.write(f"**{k}:** {v}")
        else:
            st.error("Could not map your question to a variable.")

st.sidebar.markdown("---")
st.sidebar.write("Built with ❤️ using Streamlit")
