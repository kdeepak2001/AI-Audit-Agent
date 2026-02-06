
import streamlit as st
import pandas as pd
import os
import time
from policy_engine import PolicyAgent

st.set_page_config(page_title="AI Audit Agent", page_icon="🛡️", layout="wide")

@st.cache_resource
def load_agent():
    return PolicyAgent()

st.title("🛡️ AI Internal Audit Agent")

with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.secrets.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        api_key = st.text_input("Enter Google API Key", type="password")
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
        st.success("✅ API Key Active")

uploaded_file = st.file_uploader("📂 Upload Ledger (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("1. Preview Data")
    st.dataframe(df.head())
    
    if st.button("🚀 Run AI Audit", type="primary"):
        if not api_key:
            st.error("Please provide an API Key!")
        else:
            agent = load_agent()
            with st.spinner("🧠 Reading Policy..."):
                status = agent.ingest_policy()
                st.toast(status)

            results = []
            log_container = st.container(height=300)
            
            for index, row in df.iterrows():
                query = f"Audit: ID {row['TransactionID']}, Approver {row['Approver']}, Amount ${row['Amount']}, Description: {row['Description']}"
                try:
                    decision = agent.check_policy(query)
                    is_flagged = "VIOLATION" in decision.upper()
                    status_icon = "🔴" if is_flagged else "🟢"
                    with log_container:
                        st.markdown(f"**{row['TransactionID']}** {status_icon}: {decision}")
                    results.append({"TransactionID": row['TransactionID'], "Status": "FLAGGED" if is_flagged else "PASSED", "Reasoning": decision})
                except Exception as e:
                    st.error(f"Error: {e}")
                time.sleep(0.1)

            st.dataframe(pd.DataFrame(results))
