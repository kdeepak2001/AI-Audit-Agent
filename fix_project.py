import os
import shutil

# --- 1. DEFINE THE CODE WITH THE STABLE MODEL ---

# We switched from "gemini-2.0-flash-exp" (Broken) to "gemini-1.5-flash" (Stable)
policy_engine_code = """
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate 

POLICY_PATH = "data/Company_Policy.pdf"

class PolicyAgent:
    def __init__(self):
        # STABLE MODE: Using gemini-1.5-flash
        # This model is globally available and does not give 404 errors.
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", 
            temperature=0,
            google_api_key=os.environ.get("GOOGLE_API_KEY")
        )
        self.policy_text = ""

    def ingest_policy(self):
        if not os.path.exists(POLICY_PATH):
            return "❌ Error: Policy PDF not found!"

        try:
            loader = PyPDFLoader(POLICY_PATH)
            pages = loader.load()
            self.policy_text = "\\n".join([p.page_content for p in pages])
            return "✅ Policy read successfully!"
        except Exception as e:
            return f"❌ Error reading PDF: {e}"

    def check_policy(self, query: str) -> str:
        if not self.policy_text:
            self.ingest_policy()
            
        if not self.policy_text:
            return "⚠️ Policy is empty. Please check PDF."

        prompt_template = \"\"\"
        You are a strict Internal Audit AI. Compare the transaction below against the Policy Rules.
        
        POLICY RULES:
        {policy_text}
        
        TRANSACTION TO AUDIT:
        {question}
        
        INSTRUCTIONS:
        1. If the transaction violates a rule, say "VIOLATION" and cite the specific section.
        2. If it is allowed, say "COMPLIANT".
        3. Be brief.
        
        Answer:
        \"\"\"
        
        prompt = PromptTemplate(
            template=prompt_template, 
            input_variables=["policy_text", "question"]
        )
        
        chain = prompt | self.llm
        try:
            response = chain.invoke({"policy_text": self.policy_text, "question": query})
            return response.content
        except Exception as e:
            return f"Error: {e}"
"""

app_code = """
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
"""

# --- 2. EXECUTE THE FIX ---
print("🔧 Applying Stable Model Fix...")
with open("policy_engine.py", "w", encoding="utf-8") as f:
    f.write(policy_engine_code)
with open("app.py", "w", encoding="utf-8") as f:
    f.write(app_code)

# Clean up
if os.path.exists("data/vector_db"):
    shutil.rmtree("data/vector_db")

print("🎉 SUCCESS! Switched to Gemini 1.5 Flash (Stable).")
print("👉 Please run: streamlit run app.py")