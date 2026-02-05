import pandas as pd
import os
import time
from policy_engine import PolicyAgent
from langchain_community.document_loaders import PyPDFLoader

# --- CONFIGURATION ---
DATA_DIR = "data"
LEDGER_FILE = os.path.join(DATA_DIR, "general_ledger.csv")
INVOICE_DIR = os.path.join(DATA_DIR, "invoices")
REPORT_FILE = os.path.join(DATA_DIR, "final_audit_report.csv")

def extract_invoice_text(pdf_path):
    """Extracts text from a single PDF invoice to show the AI."""
    try:
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        return " ".join([p.page_content for p in pages])
    except Exception as e:
        return f"[Error reading invoice: {e}]"

def main():
    print("[*] Starting Audit Agent...")

    # 1. Initialize the Brain
    agent = PolicyAgent()
    # Ensure the policy is indexed (The Brain needs to read the rulebook first)
    if not agent.vector_db:
        print("[*] Indexing Policy for the first time...")
        agent.ingest_policy()

    # 2. Load the General Ledger
    print(f"[*] Loading General Ledger from {LEDGER_FILE}...")
    try:
        df = pd.read_csv(LEDGER_FILE)
    except FileNotFoundError:
        print("❌ Ledger not found. Run generate_full_data.py first.")
        return

    audit_results = []

    print("\n" + "="*80)
    print(f"{'TXN ID':<12} | {'ROLE':<10} | {'AMOUNT':<10} | {'STATUS'}")
    print("="*80)

    # 3. The Audit Loop
    for index, row in df.iterrows():
        txn_id = row['TransactionID']
        approver = row['Approver']
        amount = row['Amount']
        desc = row['Description']
        
        # A. Find the Invoice PDF
        pdf_path = os.path.join(INVOICE_DIR, f"{txn_id}.pdf")
        
        # B. Read the Invoice Text (The "Evidence")
        if os.path.exists(pdf_path):
            invoice_text = extract_invoice_text(pdf_path)
        else:
            invoice_text = "[MISSING INVOICE FILE]"

        # C. Construct the Audit Query
        # We give the AI the Ledger Info + Invoice Info and ask it to check against Policy
        query = f"""
        Perform a strict 3-Way Match Audit.
        
        1. LEDGER ENTRY (Internal Record):
           - ID: {txn_id}
           - Approver: {approver}
           - Amount: ${amount}
           - Description: {desc}
           
        2. INVOICE EVIDENCE (PDF Text):
           "{invoice_text}"
           
        TASK:
        Check for two things:
        1. DATA INTEGRITY: Does the Invoice amount match the Ledger amount exactly?
        2. COMPLIANCE: Is the Approver authorized to sign for this amount based on the Policy?
        
        If valid, start with "COMPLIANT".
        If invalid, start with "VIOLATION" and explain the specific reason.
        """

        # D. Ask the Agent
        try:
            response = agent.check_policy(query)
            # Clean up text
            response_clean = response.strip().replace("\n", " ")
        except Exception as e:
            response_clean = f"AI ERROR: {e}"
        
        # E. Determine Status
        status = "🔴 FLAG" if "VIOLATION" in response_clean.upper() else "🟢 PASS"
        
        # Print to console
        role_short = approver.split()[-1] if " " in approver else approver
        print(f"{txn_id:<12} | {role_short:<10} | ${amount:<9} | {status}")
        
        # Save full explanation
        audit_results.append({
            "TransactionID": txn_id,
            "Status": status,
            "AI_Decision": response_clean
        })
        
        # Sleep to be nice to the API
        time.sleep(1)

    # 4. Save Final Report
    report_df = pd.DataFrame(audit_results)
    report_df.to_csv(REPORT_FILE, index=False)
    print("="*80)
    print(f"\n[SUCCESS] Full Audit Complete. Report saved to: {REPORT_FILE}")

if __name__ == "__main__":
    main()