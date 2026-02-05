import os
import pandas as pd
import pdfplumber
import re
from decimal import Decimal, InvalidOperation
from typing import List, Dict, Any

# --- CONFIGURATION ---
DATA_DIR = "data"
LEDGER_FILE = os.path.join(DATA_DIR, "general_ledger.csv")
INVOICE_DIR = os.path.join(DATA_DIR, "invoices")

class IngestionAgent:
    """
    The 'Eyes' of the Audit System. 
    Responsibility: Load raw data and normalize it for the Audit Core.
    """
    
    def __init__(self):
        self.ledger_df = None
        self.invoices = {} # Dictionary to hold invoice data by TransactionID

    def load_ledger(self) -> pd.DataFrame:
        """Loads the General Ledger CSV and ensures types are strict."""
        print(f"[*] Loading Ledger from {LEDGER_FILE}...")
        try:
            self.ledger_df = pd.read_csv(LEDGER_FILE)
            # Normalize column names for safety
            self.ledger_df.columns = [c.strip() for c in self.ledger_df.columns]
            print(f"   > Loaded {len(self.ledger_df)} rows.")
            return self.ledger_df
        except FileNotFoundError:
            print(f"[!] CRITICAL: Ledger file not found at {LEDGER_FILE}")
            return pd.DataFrame()

    def extract_invoice_text(self, pdf_path: str) -> str:
        """Extracts raw text from a PDF file."""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                full_text = ""
                for page in pdf.pages:
                    full_text += page.extract_text()
            return full_text
        except Exception as e:
            print(f"[!] Error reading PDF {pdf_path}: {e}")
            return ""

    def parse_invoice(self, text: str, file_name: str) -> Dict[str, Any]:
        """
        Uses Regex to find specific data points in the raw PDF text.
        In a Production (Phase 2) version, we would use an LLM here.
        For Phase 1 (Foundation), we use Regex to ensure strict control.
        """
        # 1. Extract Invoice ID (e.g., INV-1000)
        inv_id_match = re.search(r"Invoice ID:\s*(INV-\d+)", text)
        inv_id = inv_id_match.group(1) if inv_id_match else "UNKNOWN"

        # 2. Extract Total Amount (e.g., $4500.00)
        # Regex explanation: Look for '$' followed by digits and decimals
        amount_match = re.search(r"Total Amount:\s*\$([\d,]+\.\d{2})", text)
        amount = 0.0
        if amount_match:
            try:
                # Remove commas and convert to float
                clean_amount = amount_match.group(1).replace(",", "")
                amount = float(clean_amount)
            except ValueError:
                amount = 0.0

        return {
            "source_file": file_name,
            "invoice_id": inv_id,
            "extracted_amount": amount,
            "raw_text_snippet": text[:100].replace("\n", " ") + "..." # Audit trail
        }

    def run_pipeline(self):
        # 1. Load Ledger
        self.load_ledger()
        
        # 2. Process Invoices
        print(f"[*] Processing Invoices in {INVOICE_DIR}...")
        
        if not os.path.exists(INVOICE_DIR):
            print(f"[!] Directory {INVOICE_DIR} does not exist.")
            return

        invoice_files = [f for f in os.listdir(INVOICE_DIR) if f.endswith('.pdf')]
        
        results = []
        
        for f in invoice_files:
            path = os.path.join(INVOICE_DIR, f)
            # The filename contains the Transaction ID (e.g., TXN-1000.pdf)
            txn_id = f.replace(".pdf", "")
            
            raw_text = self.extract_invoice_text(path)
            structured_data = self.parse_invoice(raw_text, f)
            
            # Link to Transaction ID for the 3-Way Match later
            structured_data["linked_txn_id"] = txn_id
            results.append(structured_data)
            print(f"   > Parsed {f}: Found Amount ${structured_data['extracted_amount']}")

        return results

if __name__ == "__main__":
    agent = IngestionAgent()
    data = agent.run_pipeline()
    
    # Simple check to verify we have data
    if data:
        print("\n[SUCCESS] Phase 1 Complete. Data is structured.")
        print(f"Sample Extracted Record: {data[0]}")
    else:
        print("\n[FAIL] No data extracted.")