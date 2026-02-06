# 🛡️ AI Internal Audit Agent (Axion Ray Prototype)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![AI Model](https://img.shields.io/badge/AI-Gemini%202.0%20Flash-orange)
![Status](https://img.shields.io/badge/Status-Prototype-green)

An automated **Compliance & Warranty Audit System** powered by Generative AI. This agent ingests unstructured policy documents (PDFs) and audits financial transactions (CSVs) in real-time, flagging violations with specific policy citations.



## 🚀 Business Use Case
Manual auditing of warranty claims is slow, error-prone, and struggles with complex logic (e.g., *"Tier 2 approval required for Turbochargers under 50k km"*).

**This AI Agent solves that by:**
1.  **Ingesting** complex Policy Guidelines (PDF) dynamically.
2.  **Analyzing** structured ledger data (CSV) row-by-row.
3.  **Detecting** logic violations, banned parts, and authority limit breaches.
4.  **Citing** the exact policy section (e.g., *"Violation: Section 4.2 Mineral Oil Prohibited"*).

## 🛠️ Tech Stack
* **LLM Engine:** Google Gemini 2.0 Flash (`gemini-2.0-flash`)
* **Orchestration:** LangChain (Prompt Templates, Chains)
* **Frontend:** Streamlit (Real-time interactive UI)
* **Data Processing:** Pandas (CSV handling), PyPDFLoader (PDF ingestion)

## 📂 Project Structure
```bash
├── app.py                 # Main application interface (Streamlit)
├── policy_engine.py       # AI Logic & LangChain integration
├── requirements.txt       # Python dependencies
├── data/
│   ├── Company_Policy.pdf # The "Brain" (Warranty Rules)
│   └── warranty_claims.csv # The "Test Data" (Ledger)
└── README.md              # Documentation

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/YourUsername/Audit_Agent_Project.git](https://github.com/YourUsername/Audit_Agent_Project.git)
cd Audit_Agent_Project

### Install Dependencies
```bash
pip install -r requirements.txt

### 3. Configure API Key
* ** This project requires a Google Gemini API Key.

* **Option A (Temporary): Enter the key directly in the sidebar UI.

* **Option B (Secure - Recommended): Create a .streamlit/secrets.toml file:
```bash
GOOGLE_API_KEY = "your_api_key_here"

* **4. Run the Agent
```bash
streamlit run app.py

## ⚙️ Installation & Setup
## 🧪 How to Test (Demo Scenario)
This prototype is pre-configured with a **Powertrain Warranty Policy** (Section 4).

1.  **Launch the App.**
2.  **Upload `warranty_claims.csv`** (found in the `data/` folder).
3.  **Click "Run AI Audit".**
4.  **Observe Results:**
    * **CLM-001:** 🔴 **FLAGGED** (Turbocharger claim missing Tier 2 Approval).
    * **CLM-002:** 🔴 **FLAGGED** (Usage of banned "Mineral Oil").
    * **CLM-003:** 🔴 **FLAGGED** (Labor rate exceeds $120 cap).
    * **CLM-004:** 🟢 **PASSED** (Routine maintenance).

## 🧠 AI Architecture
Unlike standard chatbots, this system uses a **Context-Aware Inference** approach:

1.  The system reads the raw text from `Company_Policy.pdf`.
2.  It constructs a dynamic prompt injecting the **Policy Rules** as the "Ground Truth".
3.  It iterates through the **CSV Ledger**, passing each transaction as a "Query".
4.  The LLM acts as a strict auditor, returning a binary `VIOLATION` / `COMPLIANT` decision with reasoning.



## 🤝 Contributing
Open to contributions! Please fork the repo and submit a PR.

## 📄 License
MIT License