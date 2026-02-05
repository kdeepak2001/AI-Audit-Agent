import streamlit as st
import pandas as pd
import os

# Page Config
st.set_page_config(page_title="AI Audit Agent", layout="wide")

st.title("🛡️ AI Internal Audit Agent")
st.markdown("### Powered by Gemini 2.0 Flash & LangChain")
st.info("This agent performs a 3-Way Match: Ledger vs. Invoice vs. Policy.")

# Paths
REPORT_FILE = "data/final_audit_report.csv"
LEDGER_FILE = "data/general_ledger.csv"

# Tabs
tab1, tab2 = st.tabs(["📊 Audit Dashboard", "📂 Raw Data"])

with tab1:
    if os.path.exists(REPORT_FILE):
        df = pd.read_csv(REPORT_FILE)

        # Metrics
        total = len(df)
        flagged = len(df[df['Status'].str.contains("FLAG")])
        passed = total - flagged

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Transactions", total)
        col2.metric("✅ Passed", passed)
        col3.metric("🔴 Flagged", flagged)

        st.divider()

        # Display Flags with Explanations
        st.subheader("🔴 Flagged Transactions (Requires Review)")
        flags = df[df['Status'].str.contains("FLAG")]

        if not flags.empty:
            for index, row in flags.iterrows():
                with st.expander(f"Transaction {row['TransactionID']} - {row['Status']}"):
                    st.write(f"**AI Explanation:** {row['AI_Decision']}")
        else:
            st.success("No violations found!")

    else:
        st.warning("No Audit Report found. Please run the audit first.")

with tab2:
    st.subheader("General Ledger Data")
    if os.path.exists(LEDGER_FILE):
        ledger = pd.read_csv(LEDGER_FILE)
        st.dataframe(ledger)