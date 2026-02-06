import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate 

# --- CONFIGURATION ---
POLICY_PATH = "data/Company_Policy.pdf"

class PolicyAgent:
    def __init__(self):
        # FIX: We use the EXACT model name found in your list
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash", 
            temperature=0,
            google_api_key=os.environ.get("GOOGLE_API_KEY")
        )
        self.policy_text = ""

    def ingest_policy(self):
        """Reads the PDF directly into text"""
        if not os.path.exists(POLICY_PATH):
            return "❌ Error: Policy PDF not found!"

        try:
            loader = PyPDFLoader(POLICY_PATH)
            pages = loader.load()
            # Combine all pages into one simple text string
            self.policy_text = "\n".join([p.page_content for p in pages])
            return "✅ Policy read successfully!"
        except Exception as e:
            return f"❌ Error reading PDF: {e}"

    def check_policy(self, query: str) -> str:
        """Asks Gemini to check the policy text directly"""
        
        # If policy hasn't been read yet, read it now
        if not self.policy_text:
            self.ingest_policy()
            
        if not self.policy_text:
            return "⚠️ Policy is empty. Please check the PDF."

        # Direct Prompting
        prompt_template = """
        You are a strict Internal Audit AI. Compare the transaction below against the Policy Rules.
        
        POLICY RULES:
        {policy_text}
        
        TRANSACTION TO AUDIT:
        {question}
        
        INSTRUCTIONS:
        1. If the transaction violates a rule, say "VIOLATION" and cite the specific section (e.g., Section 4.1).
        2. If it is allowed, say "COMPLIANT".
        3. Be brief and professional.
        
        Answer:
        """
        
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