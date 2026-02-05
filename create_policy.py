from fpdf import FPDF
import os

# Ensure the data directory exists
if not os.path.exists("data"):
    os.makedirs("data")

POLICY_FILE = "data/Company_Policy.pdf"

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# Title
pdf.set_font("Arial", 'B', 16)
pdf.cell(200, 10, txt="Global Expense & Procurement Policy", ln=1, align='C')
pdf.ln(10)

# Section 1: Delegation of Authority
pdf.set_font("Arial", 'B', 14)
pdf.cell(200, 10, txt="1. Delegation of Authority (DoA)", ln=1)
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, txt="""
1.1 Managers are authorized to approve expenses up to $1,000 USD.
1.2 Directors are authorized to approve expenses up to $5,000 USD.
1.3 Vice Presidents (VPs) are authorized to approve expenses up to $10,000 USD.
1.4 Any expense above $10,000 USD requires C-Level approval.
""")
pdf.ln(5)

# Section 2: Segregation of Duties
pdf.set_font("Arial", 'B', 14)
pdf.cell(200, 10, txt="2. Segregation of Duties (SoD)", ln=1)
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, txt="""
2.1 The individual requesting an expense/purchase cannot be the same individual who approves it.
2.2 Self-approval is strictly prohibited under all circumstances.
""")
pdf.ln(5)

# Section 3: Documentation
pdf.set_font("Arial", 'B', 14)
pdf.cell(200, 10, txt="3. Documentation Requirements", ln=1)
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, txt="""
3.1 All invoices must match the General Ledger amount exactly.
3.2 A variance of $0.01 is acceptable for rounding errors.
3.3 Invoices must be submitted within 30 days of service.
""")

pdf.output(POLICY_FILE)
print(f"[SUCCESS] Policy Manual created at: {POLICY_FILE}")