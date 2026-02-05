import os
import time
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate 

# Compatibility import for RetrievalQA
try:
    from langchain_classic.chains import RetrievalQA
except ImportError:
    from langchain.chains import RetrievalQA

# --- CONFIGURATION ---
POLICY_PATH = "data/Company_Policy.pdf"
DB_PATH = "data/vector_db"

class PolicyAgent:
    def __init__(self):
        print("[*] Initializing Policy Agent (Gemini 2.0 Mode)...")
        
        if "GOOGLE_API_KEY" not in os.environ:
             print("[!] CRITICAL: GOOGLE_API_KEY is missing. Run 'set GOOGLE_API_KEY=...'")
        
        # 1. EMBEDDINGS
        # Your logs showed this part works fine, so we keep it.
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        
        self.vector_db = None
        
        # 2. LLM: SWITCHED TO YOUR AVAILABLE MODEL
        # We selected 'gemini-2.0-flash' from your diagnostic list.
        self.llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash", temperature=0)

    def ingest_policy(self):
        """Reads PDF and builds the Vector Database"""
        if not os.path.exists(POLICY_PATH):
            print(f"[!] Policy file missing: {POLICY_PATH}")
            return

        print(f"[*] Indexing Policy Document: {POLICY_PATH}")
        loader = PyPDFLoader(POLICY_PATH)
        pages = loader.load_and_split()
        
        print(f"[*] Sending {len(pages)} pages to Cloud Embeddings...")
        
        try:
            self.vector_db = FAISS.from_documents(pages, self.embeddings)
            self.vector_db.save_local(DB_PATH)
            print("[*] Policy Knowledge Base built and saved.")
        except Exception as e:
            print(f"[!] API Warning: {e}")
            print("[*] Retrying in 5s...")
            time.sleep(5)
            self.vector_db = FAISS.from_documents(pages, self.embeddings)
            self.vector_db.save_local(DB_PATH)
            print("[*] Success on Retry.")

    def check_policy(self, query: str) -> str:
        """Asks the AI a question based strictly on the policy."""
        if not self.vector_db:
            if os.path.exists(DB_PATH):
                self.vector_db = FAISS.load_local(DB_PATH, self.embeddings, allow_dangerous_deserialization=True)
            else:
                return "Error: Policy DB not found. Run ingest_policy() first."

        prompt_template = """
        You are a Strict Internal Auditor. Answer the question based ONLY on the context below.
        If the action violates policy, start with "VIOLATION:".
        If it is allowed, start with "COMPLIANT:".
        Cite the specific section number (e.g., 1.2).

        Context: {context}

        Question: {question}
        
        Answer:
        """
        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_db.as_retriever(),
            chain_type_kwargs={"prompt": prompt}
        )
        
        # Using invoke (Modern LangChain standard)
        result = qa_chain.invoke(query)
        return result['result']

if __name__ == "__main__":
    # TEST RUN
    agent = PolicyAgent()
    agent.ingest_policy()
    
    test_q = "A Director approved an invoice for $6,000. Is this allowed?"
    print(f"\nQuestion: {test_q}")
    print(f"AI Decision: {agent.check_policy(test_q)}")