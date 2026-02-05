# 🛡️ AI Internal Audit Agent
### Autonomous, Policy-Aware Financial Compliance for the AI Era

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-audit-agent-4roq5eor4h4cjd8cr9pb6b.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Gemini](https://img.shields.io/badge/AI-Gemini%202.0%20Flash-4285F4)
![LangChain](https://img.shields.io/badge/Framework-LangChain-green)
![FAISS](https://img.shields.io/badge/Vector_DB-FAISS-orange)

---

## 📋 Executive Summary

The **AI Internal Audit Agent** is an **enterprise-grade, autonomous compliance system** that automates internal financial audits using **policy-grounded AI reasoning**.

Traditional audits are manual, slow, and reactive. This agent transforms auditing into a **real-time, explainable, and scalable process** by validating every transaction against official corporate policies using a **Retrieval-Augmented Generation (RAG)** architecture.

> A virtual internal auditor that never skips rules and always shows its reasoning.

🔗 **Live App:** [Click here to try the Live Demo](https://ai-audit-agent-4roq5eor4h4cjd8cr9pb6b.streamlit.app/)

---

## 🎯 Problem Statement

Organizations face audit risks due to:
- Manual approval checks
- Inconsistent policy interpretation
- Delayed violation detection
- High operational audit costs

This system embeds **policy intelligence directly into the transaction review process**, enabling continuous and automated audits.

---

## 🏗️ System Architecture (RAG-Based)

The agent follows a **Retrieval-Augmented Generation (RAG)** architecture to ensure **every decision is grounded in internal policy**, not general LLM knowledge.

### 🔄 Data Flow

1. **Policy Ingestion**
   - Policy PDFs are chunked and embedded
   - Stored in a local **FAISS vector database**

2. **Transaction Input**
   - General Ledger (CSV / Excel)
   - Optional invoice text (PDF / OCR)

3. **Policy Retrieval**
   - Relevant policy sections are retrieved dynamically
   - Example: *Director approval limits*

4. **AI Reasoning**
   - **Gemini 2.0 Flash** evaluates transactions against policy

5. **Audit Output**
   - Each transaction is labeled:
     - ✅ `COMPLIANT`
     - ❌ `VIOLATION`
   - Results displayed and exportable

---

## ✅ Core Audit Logic — The “3-Way Match”

### 1️⃣ Policy Compliance Check
**Input:** “A Director approved an invoice for $6,000.”

**Retrieved Policy:** “Directors may approve invoices up to $5,000.”

**Decision:** $6,000 > $5,000 → ❌ **VIOLATION**

---

### 2️⃣ Data Integrity Check
- Ledger Amount: $200
- Invoice Amount: $250

Mismatch detected → ❌ **VIOLATION**

---

### 3️⃣ Explainability
Every decision is:
- Traceable to a policy clause
- Numerically justified
- Ready for audit review

---

## ✨ Key Features

- 📄 **Policy-Aware AI (No Hallucinations)**
- 🔁 **Dynamic Policy Updates**
- ⚡ **High-Speed Batch Auditing**
- 🧩 **Multi-Modal Inputs**
- 📊 **Interactive Streamlit Dashboard**

---

## 🛠️ Tech Stack

| Layer | Technology |
|------|-----------|
| LLM | Google Gemini 2.0 Flash |
| Framework | LangChain |
| Vector Store | FAISS |
| Frontend | Streamlit |
| Language | Python 3.10+ |

---

## ⚙️ Local Installation

### 1️⃣ Clone Repository
```bash
git clone [https://github.com/kdeepak2001/AI-Audit-Agent.git](https://github.com/kdeepak2001/AI-Audit-Agent.git)
cd AI-Audit-Agent

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt

### 3️⃣ Set API Key
```bash
export GOOGLE_API_KEY="your_api_key_here"

### 4️⃣ Run Application
```bash
streamlit run app.py

## 🔮 Roadmap

Phase 2: Vision-based OCR for scanned invoices
Phase 3: ERP integrations (SAP, Oracle NetSuite)
Phase 4: Multi-language policy auditing
Phase 5: Automated alerts and escalation workflows

## 👤 Author & Contact

### 🌐 GitHub: github.com/kdeepak2001

## 🔗 LinkedIn: linkedin.com/in/kalava-deepak

## 📧 Email: kalavadeepak2001@gmail.com

## 📱 Mobile: +91-9502684256

## 🧠 Why This Project Matters
### This project demonstrates:

Responsible AI through policy grounding.

Explainable, deterministic decision-making.

Enterprise-ready RAG architecture.

Practical AI applied to real compliance problems.
This is not a chatbot. This is an AI-powered audit system.