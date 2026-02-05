import os
import pandas as pd
from fpdf import FPDF
from datetime import datetime, timedelta

# --- CONFIGURATION ---
DATA_DIR = "data"
LEDGER_FILE = os.path.join(DATA_DIR, "general_ledger.csv")
INVOICE_DIR = os.path.join(DATA_DIR, "invoices")

# Ensure directories exist
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
if not os.path.exists(INVOICE_DIR):
    os.makedirs(INVOICE_DIR)

# --- MOCK DATA ---
transactions = [
    # Case 1: Perfect Match (Pass)
    {"vendor": "TechCorp Solutions", "amount": 4500.00, "approver": "Bob Director", "desc": "Server Maintenance"},
    # Case 2: DoA Violation (Fail - Director approving > $5k)
    {"vendor": "Global Consultants", "amount": 6000.00, "approver": "Bob Director", "desc": "Strategy Audit"},
    # Case 3: Amount Mismatch (Fail - Ledger says 200, Invoice will say 250)
    {"vendor": "Office Supplies Co", "amount": 200.00, "approver": "Charlie Manager", "desc": "Paper Supplies"},
]

ledger_data = []

print("[*] Generating General Ledger & Invoices...")

for i, tx in enumerate(transactions):
    tx_id = f"TXN-{1000+i}"
    date_str = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
    
    # 1. Add to Ledger Data
    ledger_entry = {
        "TransactionID": tx_id,
        "Date": date_str,
        "Vendor": tx["vendor"],
        "Amount": tx["amount"],
        "Currency": "USD",
        "Approver": tx["approver"],
        "Description": tx["desc"]
    }
    ledger_data.append(ledger_entry)

    # 2. Generate PDF Invoice
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"INVOICE - {tx['vendor']}", ln=1, align='C')
    pdf.ln(10)
    
    # Details
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Invoice ID: INV-{1000+i}", ln=1)
    pdf.cell(200, 10, txt=f"Date: {date_str}", ln=1)
    pdf.cell(200, 10, txt="Bill To: Your Company Inc.", ln=1)
    pdf.ln(10)
    
    # Line Items
    # TRICK: For Case 3, we write a DIFFERENT amount in the PDF to test the AI
    invoice_amount = tx["amount"]
    if i == 2: # The mismatch case
        invoice_amount = 250.00 
        
    pdf.cell(200, 10, txt=f"Description: {tx['desc']}", ln=1)
    pdf.cell(200, 10, txt=f"Total Amount: ${invoice_amount:.2f}", ln=1)
    
    # Footer
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 10, txt="Payment due within 30 days.", ln=1)
    
    # Save PDF
    pdf_path = os.path.join(INVOICE_DIR, f"{tx_id}.pdf")
    pdf.output(pdf_path)
    print(f"    -> Created Invoice: {pdf_path}")

# Save Ledger CSV
df = pd.DataFrame(ledger_data)
df.to_csv(LEDGER_FILE, index=False)
print(f"[SUCCESS] General Ledger saved to {LEDGER_FILE}")