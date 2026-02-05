\# 🛡️ AI Internal Audit Agent



\[!\[Streamlit App](https://static.streamlit.io/badges/streamlit\_badge\_black\_white.svg)](https://ai-audit-agent-4roq5eor4h4cjd8cr9pb6b.streamlit.app/)

!\[Python](https://img.shields.io/badge/Python-3.10%2B-blue)

!\[Gemini](https://img.shields.io/badge/AI-Gemini%202.0%20Flash-4285F4)

!\[LangChain](https://img.shields.io/badge/Framework-LangChain-green)

!\[FAISS](https://img.shields.io/badge/Vector\_DB-FAISS-orange)



\## 📋 Executive Summary

The \*\*AI Internal Audit Agent\*\* is an enterprise-grade compliance tool designed to automate the \*\*"3-Way Match"\*\* audit process. Traditional auditing is manual, slow, and error-prone. This agent acts as an autonomous virtual auditor that validates financial transactions against internal corporate policies in real-time.



\*\*\[Click here to try the Live App](https://ai-audit-agent-4roq5eor4h4cjd8cr9pb6b.streamlit.app/)\*\*



---



\## 🏗️ System Architecture



The system follows a \*\*Retrieval-Augmented Generation (RAG)\*\* architecture to ensure decisions are grounded in the specific company policy, rather than general knowledge.



\*\*The Data Flow:\*\*

1\.  \*\*Ingestion Layer:\*\* The `PolicyAgent` loads the corporate policy (PDF), splits it into chunks, and converts them into vector embeddings using Google's embedding model. These are stored in a local \*\*FAISS Vector Database\*\*.

2\.  \*\*Input Layer:\*\* The user uploads a General Ledger (CSV/Excel) via the Streamlit interface.

3\.  \*\*Orchestration Layer:\*\* For every transaction row, the system:

&nbsp;   \* Retrieves the specific policy section relevant to the user's role (e.g., "Director limits").

&nbsp;   \* Constructs a dynamic prompt containing the \*Transaction Data\* + \*Retrieved Policy Rule\*.

4\.  \*\*Cognitive Layer:\*\* The \*\*Gemini 2.0 Flash\*\* model analyzes the prompt and determines if the transaction is `COMPLIANT` or a `VIOLATION`.

5\.  \*\*Presentation Layer:\*\* Results are visualized in real-time on the dashboard and exported as a CSV report.



---



\## 🧠 Core Logic: The "3-Way Match"

The agent does not just "guess"; it strictly adheres to a logical verification process modeled after human auditors:



\### 1. The Policy Check (RAG)

\* \*\*Input:\*\* "A Director approved $6,000."

\* \*\*Retrieval:\*\* The system searches the Vector DB for "Director approval limits."

\* \*\*Context:\*\* It finds Section 1.2: \*"Directors may approve up to $5,000."\*

\* \*\*Decision:\*\* Since $6,000 > $5,000 -> \*\*FLAGGED\*\*.



\### 2. The Data Integrity Check

\* \*\*Input:\*\* Ledger says $200. Invoice (OCR text) says $250.

\* \*\*Comparison:\*\* The AI compares the two values numerically.

\* \*\*Decision:\*\* Values do not match -> \*\*FLAGGED\*\*.



---



\## 🚀 Key Features

\* \*\*📄 Dynamic Policy Learning:\*\* The AI isn't hard-coded. Update the PDF policy file, and the AI automatically "learns" the new rules on the next run.

\* \*\*👁️ Multi-Modal Analysis:\*\* Capable of processing unstructured text from invoices and structured data from CSVs simultaneously.

\* \*\*⚡ High-Speed Batch Processing:\*\* Audits hundreds of transactions in minutes, providing immediate feedback via a progress bar.

\* \*\*📊 Interactive Dashboard:\*\* A user-friendly Streamlit UI that requires no coding knowledge to operate.



---



\## 🔮 Future Roadmap

We are continuously improving the Audit Agent. Upcoming features include:



\* \*\*Phase 2: Vision-Based OCR:\*\* Integrating \*\*Gemini Pro Vision\*\* to read scanned/handwritten receipts directly (currently processes text-based PDFs).

\* \*\*Phase 3: ERP Integration:\*\* Direct API connectors for SAP and Oracle NetSuite to fetch live ledger data without CSV uploads.

\* \*\*Phase 4: Multi-Language Support:\*\* Enabling the agent to audit invoices in Spanish, French, and German using translation embeddings.

\* \*\*Phase 5: Auto-Email Alerts:\*\* Automatically notifying the specific approver via SMTP when a transaction is flagged.



---



\## 🛠️ Tech Stack

\* \*\*LLM:\*\* Google Gemini 2.0 Flash

\* \*\*Framework:\*\* LangChain

\* \*\*Vector Store:\*\* FAISS

\* \*\*Frontend:\*\* Streamlit

\* \*\*Environment:\*\* Python 3.10+



\## ⚙️ Installation (Local Dev)



1\.  \*\*Clone the Repository\*\*

&nbsp;   ```bash

&nbsp;   git clone \[https://github.com/kdeepak2001/AI-Audit-Agent.git](https://github.com/kdeepak2001/AI-Audit-Agent.git)

&nbsp;   cd AI-Audit-Agent

&nbsp;   ```



2\.  \*\*Install Dependencies\*\*

&nbsp;   ```bash

&nbsp;   pip install -r requirements.txt

&nbsp;   ```



3\.  \*\*Set Up API Keys\*\*

&nbsp;   \* Export your key in your terminal:

&nbsp;   \* `export GOOGLE\_API\_KEY="your\_api\_key\_here"`



4\.  \*\*Run the App\*\*

&nbsp;   ```bash

&nbsp;   streamlit run app.py

&nbsp;   ```



---

\*Built by K Deepak\*

