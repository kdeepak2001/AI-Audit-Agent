import streamlit as st
import pandas as pd
import os
import time
from policy_engine import PolicyAgent

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Audit Agent", page_icon="🛡️", layout="wide")

# --- CACHED RESOURCES (Speed Optimization) ---
# This prevents reloading the AI model every time you click a button
@st.cache_resource
def load_agent():
    return PolicyAgent()

# --- HEADER ---
st.title("🛡️ AI Internal Audit Agent")
st.markdown("""
**Upload your financial ledger below.** The AI will check every transaction against the
internal policy (Delegation of Authority) and flag suspicious approvals.
""")

# --- SIDEBAR (Controls) ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # 1. API Key Handling (For Cloud Deployment)
    # Check if key is in Secrets (Cloud) or Environment (Local)
    api_key = st.secrets.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    
    if not api_key:
        api_key = st.text_input("Enter Google API Key", type="password")
        if api_key:
            os.environ["GOOGLE_API_KEY"] = api_key
    
    if api_key:
        st.success("✅ API Key Active")
    else:
        st.warning("⚠️ Please enter API Key to run audit")

    st.divider()
    st.info("Built with Gemini 2.0 Flash & LangChain")

# --- MAIN INTERFACE ---

# 1. File Uploader
uploaded_file = st.file_uploader("📂 Upload Ledger (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file:
    # Load the data
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.subheader("1. Preview Data")
        st.dataframe(df.head())
        
        # Validation: Check if necessary columns exist
        required_cols = ['TransactionID', 'Amount', 'Approver', 'Description']
        missing = [col for col in required_cols if col not in df.columns]
        
        if missing:
            st.error(f"❌ Missing columns: {', '.join(missing)}. Please check your file format.")
        else:
            # 2. Run Audit Button
            if st.button("🚀 Run AI Audit", type="primary"):
                if not api_key:
                    st.error("Please provide an API Key first!")
                else:
                    agent = load_agent()
                    
                    # Ensure Policy is Loaded
                    if not agent.vector_db:
                        with st.spinner("🧠 Reading Policy Rules..."):
                            agent.ingest_policy()

                    # audit loop
                    results = []
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    total_rows = len(df)
                    
                    st.subheader("2. Real-Time Audit Logs")
                    log_container = st.container(height=300)

                    for index, row in df.iterrows():
                        # Update UI
                        status_text.text(f"Auditing Transaction {row['TransactionID']}...")
                        progress_bar.progress((index + 1) / total_rows)
                        
                        # Formulate Query
                        query = f"""
                        Audit this transaction against the Policy:
                        - ID: {row['TransactionID']}
                        - Approver: {row['Approver']}
                        - Amount: ${row['Amount']}
                        - Description: {row['Description']}
                        
                        Is this a VIOLATION or COMPLIANT? Explain briefly.
                        """
                        
                        # Ask AI
                        try:
                            decision = agent.check_policy(query)
                            decision = decision.replace("\n", " ")
                        except Exception as e:
                            decision = f"Error: {e}"
                        
                        # Determine Status
                        is_flagged = "VIOLATION" in decision.upper()
                        status_icon = "🔴" if is_flagged else "🟢"
                        
                        # Log to UI
                        with log_container:
                            st.markdown(f"**{row['TransactionID']}** {status_icon}: {decision}")

                        results.append({
                            "TransactionID": row['TransactionID'],
                            "Approver": row['Approver'],
                            "Amount": row['Amount'],
                            "Status": "FLAGGED" if is_flagged else "PASSED",
                            "AI_Reasoning": decision
                        })
                        
                        # Rate limit safety
                        time.sleep(0.5)

                    status_text.text("Audit Complete!")
                    
                    # 3. Final Report
                    st.divider()
                    st.subheader("3. Audit Results")
                    
                    result_df = pd.DataFrame(results)
                    
                    # Metrics
                    col1, col2 = st.columns(2)
                    col1.metric("Total Audited", len(result_df))
                    col2.metric("Violations Found", len(result_df[result_df['Status']=="FLAGGED"]))
                    
                    # Show Data
                    st.dataframe(result_df)
                    
                    # Download Button
                    csv = result_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Audit Report",
                        data=csv,
                        file_name="audit_report_ai.csv",
                        mime="text/csv",
                    )

    except Exception as e:
        st.error(f"Error reading file: {e}")

else:
    # Default State (Show instructions)
    st.info("👋 Upload a CSV file to begin. Expect columns: TransactionID, Amount, Approver, Description")
    
    # Create a dummy template for them to download
    dummy_data = {
        "TransactionID": ["TXN-001", "TXN-002"],
        "Amount": [4000, 6000],
        "Approver": ["Manager", "Manager"],
        "Description": ["Office Supplies", "Server Purchase"]
    }
    df_template = pd.DataFrame(dummy_data)
    csv_template = df_template.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 Download Sample Template",
        data=csv_template,
        file_name="ledger_template.csv",
        mime="text/csv"
    )