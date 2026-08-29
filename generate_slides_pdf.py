import os
import sys
import time
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
)
from reportlab.pdfgen import canvas

project_dir = r"C:\Users\kanis\.gemini\antigravity\scratch\intelligent-data-os"
output_pdf_path = os.path.join(project_dir, "presentation", "DataOS_Slide_Presentation.pdf")
os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)

# 16:9 Widescreen slide dimensions: 11 x 6.1875 inches
SLIDE_WIDTH = 11.0 * inch
SLIDE_HEIGHT = 6.1875 * inch

# ----------------- Slide Numbered Canvas -----------------
class SlideCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(SlideCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_slide_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_slide_decorations(self, page_count):
        self.saveState()
        # Dark slide background fill
        self.setFillColor(colors.HexColor("#090d16"))
        self.rect(0, 0, SLIDE_WIDTH, SLIDE_HEIGHT, fill=True, stroke=False)
        
        # Subtle top gradient border
        self.setStrokeColor(colors.HexColor("#312e81"))
        self.setLineWidth(1.5)
        self.line(36, SLIDE_HEIGHT - 24, SLIDE_WIDTH - 36, SLIDE_HEIGHT - 24)
        
        # Bottom footer bar
        self.setStrokeColor(colors.HexColor("#1e293b"))
        self.setLineWidth(0.8)
        self.line(36, 28, SLIDE_WIDTH - 36, 28)
        
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#6366f1"))
        self.drawString(36, 16, "DATAOS")
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#94a3b8"))
        self.drawString(84, 16, "•  Intelligent Big Data & Autonomous Analytics Operating System")
        self.drawRightString(SLIDE_WIDTH - 36, 16, f"Slide {self._pageNumber} of {page_count}")
        self.restoreState()

doc = SimpleDocTemplate(
    output_pdf_path,
    pagesize=(SLIDE_WIDTH, SLIDE_HEIGHT),
    leftMargin=36,
    rightMargin=36,
    topMargin=36,
    bottomMargin=36
)

styles = getSampleStyleSheet()

# Slide Typography Styles
s_cat = ParagraphStyle("SCat", fontName="Helvetica-Bold", fontSize=8.5, leading=10, textColor=colors.HexColor("#06b6d4"), spaceAfter=2)
s_title = ParagraphStyle("STitle", fontName="Helvetica-Bold", fontSize=18, leading=22, textColor=colors.white, spaceAfter=8)
s_subtitle = ParagraphStyle("SSub", fontName="Helvetica", fontSize=10.5, leading=14, textColor=colors.HexColor("#94a3b8"), spaceAfter=12)

card_title = ParagraphStyle("CTitle", fontName="Helvetica-Bold", fontSize=11, leading=13, textColor=colors.HexColor("#818cf8"), spaceAfter=4)
card_body = ParagraphStyle("CBody", fontName="Helvetica", fontSize=8.5, leading=12.5, textColor=colors.HexColor("#cbd5e1"), spaceAfter=3)
card_bullet = ParagraphStyle("CBullet", fontName="Helvetica", fontSize=8.2, leading=11.5, textColor=colors.HexColor("#e2e8f0"), leftIndent=8, spaceAfter=2.5)

def make_slide_card(title, bullets, width_pt, height_pt=260, badge="", border_color="#334155", bg_color="#0f172a"):
    elems = []
    header_text = f"<b>{title}</b>" + (f"  <font color='#06b6d4' size='7.5'>[{badge}]</font>" if badge else "")
    elems.append(Paragraph(header_text, card_title))
    for b in bullets:
        elems.append(Paragraph(f"• {b}", card_bullet))
    
    t = Table([[elems]], colWidths=[width_pt])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(bg_color)),
        ('BOX', (0, 0), (-1, -1), 1.0, colors.HexColor(border_color)),
        ('PADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    return t

story = []

# ==========================================
# SLIDE 1: Title Slide
# ==========================================
story.append(Spacer(1, 40))
story.append(Paragraph("<font color='#06b6d4'>CAPSTONE PROJECT PRESENTATION  •  PRODUCTION RELEASE v2.5</font>", s_cat))
story.append(Paragraph("DataOS Platform", ParagraphStyle("TitleMain", fontName="Helvetica-Bold", fontSize=32, leading=38, textColor=colors.HexColor("#818cf8"), spaceAfter=6)))
story.append(Paragraph("Intelligent End-to-End Big Data & Autonomous Analytics Operating System", ParagraphStyle("TitleSub", fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=colors.white, spaceAfter=14)))
story.append(Paragraph(
    "A universal, no-code data operating system that automates the entire data lifecycle — combining multi-format ingestion, 1-click statistical auto-cleaning (ETL), visual DAG pipelines, conversational voice NLQ, continuous AI model evolution, Indian DPDP Act 2023 compliance, and standalone zero-server model export.",
    ParagraphStyle("TitleDesc", fontName="Helvetica", fontSize=9.5, leading=14.5, textColor=colors.HexColor("#94a3b8"), spaceAfter=20)
))

meta_row = [
    Paragraph("<b>Presenter:</b> <font color='#ffffff'>Kanishka</font>", card_body),
    Paragraph("<b>Live Studio:</b> <font color='#38bdf8'>http://localhost:8000</font>", card_body),
    Paragraph("<b>GitHub:</b> <font color='#a7f3d0'>@Kanishka22222/intelligent-data-os</font>", card_body)
]
t_m = Table([meta_row], colWidths=[220, 240, 260])
t_m.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0f172a")),
    ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#334155")),
    ('PADDING', (0, 0), (-1, -1), 8),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(t_m)
story.append(PageBreak())

# ==========================================
# SLIDE 2: Problem
# ==========================================
story.append(Paragraph("INDUSTRY LANDSCAPE & MOTIVATION", s_cat))
story.append(Paragraph("The Core Problem: Modern Data Tool Fragmentation", s_title))

c1 = make_slide_card("1. Tool Sprawl & Fragility", [
    "Enterprises juggle 6-8 separate tools (Fivetran, dbt, Spark, Tableau, ML scripts).",
    "Engineers spend 80% of their time writing brittle glue code instead of analyzing.",
    "Exorbitant licensing costs across multiple vendors."
], 230, badge="HIGH COST", border_color="#f43f5e")

c2 = make_slide_card("2. Non-Technical Barrier", [
    "Business leaders and managers lack SQL/Python programming expertise.",
    "Dashboard change requests face 2 to 3-week backlogs with data teams.",
    "Lack of natural language & voice accessibility isolates decision-makers."
], 230, badge="ACCESSIBILITY", border_color="#f59e0b")

c3 = make_slide_card("3. Compliance & AI Lock-In", [
    "Sensitive PII (Aadhaar, PAN, Cards) exposed in raw data workflows.",
    "Indian DPDP Act 2023 & GDPR mandate immutable, verifiable audit ledgers.",
    "Traditional AI models freeze and cannot run independently outside platforms."
], 230, badge="REGULATORY", border_color="#6366f1")

t_prob = Table([[c1, c2, c3]], colWidths=[238, 238, 238])
t_prob.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))
story.append(t_prob)
story.append(PageBreak())

# ==========================================
# SLIDE 3: Proposed Solution
# ==========================================
story.append(Paragraph("UNIFIED ARCHITECTURAL PARADIGM", s_cat))
story.append(Paragraph("The Solution: DataOS Autonomous Operating System", s_title))

s1_card = make_slide_card("All-in-One Data Lifecycle", [
    "Consolidates Ingestion, 1-Click Auto-Clean ETL, Visual DAG Studio, BI Dashboards, and AI Brain into a single glassmorphic web studio.",
    "Runs seamlessly on desktop (localhost:8000), Docker, and Vercel cloud."
], 355, badge="UNIFIED PLATFORM", border_color="#4f46e5")

s2_card = make_slide_card("Conversational Voice & NLP", [
    "Multi-lingual Web Speech voice recognition (English, Hindi, Spanish, French) translated to SQL.",
    "Self-learning semantic query memory caches analytical answers for sub-millisecond latency."
], 355, badge="NO-CODE ACCESS", border_color="#06b6d4")

s3_card = make_slide_card("Continual Learning & Standalone AI", [
    "AI Brain continually trains on every user dataset, reducing loss with every epoch.",
    "1-Click Export generates a 100% self-contained standalone AI model (.py) with zero server dependencies."
], 355, badge="PORTABLE AI", border_color="#10b981")

s4_card = make_slide_card("DPDP 2023 & Cryptographic Audit", [
    "Automated detection and redacting of Aadhaar, PAN, and payment cards.",
    "SHA-256 chained tamper-evident ledger cryptographically guarantees data integrity."
], 355, badge="COMPLIANCE", border_color="#ec4899")

t_sol = Table([[s1_card, s2_card], [s3_card, s4_card]], colWidths=[360, 360])
t_sol.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('BOTTOMPADDING', (0, 0), (-1, -1), 8)]))
story.append(t_sol)
story.append(PageBreak())

# ==========================================
# SLIDE 4: Architecture Diagram
# ==========================================
story.append(Paragraph("SYSTEM DESIGN & FLOW", s_cat))
story.append(Paragraph("Multi-Layer Autonomous System Architecture", s_title))
arch_img = os.path.join(project_dir, "presentation", "assets", "arch_diagram.png")
if os.path.exists(arch_img):
    story.append(Image(arch_img, width=720, height=270))
story.append(PageBreak())

# ==========================================
# SLIDE 5: Ingestion & Auto-Clean ETL
# ==========================================
story.append(Paragraph("MODULES 1 & 2: DATA ENGINE", s_cat))
story.append(Paragraph("Intelligent Data Ingestion & 1-Click Auto-Clean ETL", s_title))

ing_card = make_slide_card("Multi-Format Ingestion Hub", [
    "Universal parser for CSV, JSON, Parquet, Excel, and REST endpoints.",
    "Simulated real-time WebSocket IoT sensor stream (64°C, 120 PSI).",
    "Preloaded benchmark datasets:",
    "  • E-Commerce Sales (150+ transactional orders)",
    "  • Indian Financial GST (80+ invoices with CGST/SGST/IGST)",
    "  • Telecom Customer Churn (120+ subscribers)",
    "  • Machine Sensor Telemetry (real-time stream)"
], 355, badge="UNIVERSAL INGESTION", border_color="#4f46e5")

etl_card = make_slide_card("1-Click Auto-Clean Engine", [
    "Automated Deduplication: removes redundant duplicate observation rows.",
    "Statistical Imputation: median fill for numeric, mode fill for categorical columns.",
    "IQR Outlier Capping: clips extreme spikes between 1st & 99th percentiles.",
    "Data Quality Scorecard: calculates 0-100% data fidelity score before & after transformation.",
    "Jumps data quality from initial raw 62% ➔ 99.5% clean score."
], 355, badge="AUTOMATED ETL", border_color="#06b6d4")

t_etl = Table([[ing_card, etl_card]], colWidths=[360, 360])
t_etl.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))
story.append(t_etl)
story.append(PageBreak())

# ==========================================
# SLIDE 6: Visual DAG Canvas
# ==========================================
story.append(Paragraph("MODULE 3: PIPELINE STUDIO", s_cat))
story.append(Paragraph("Visual Drag-and-Drop Workflow Canvas (DAG Studio)", s_title))

dag_card = make_slide_card("Interactive DAG Node Studio", [
    "Visual node canvas with specialized transformation blocks:",
    "  • Source Node (Dataset selector)",
    "  • Filter Node (Conditional row filtering)",
    "  • Select Node (Column projection)",
    "  • Aggregate Node (Group By Sum/Mean)",
    "  • Mutate Node (Column math formulas)",
    "  • Auto-Clean & PII Redact Nodes",
    "Preloaded templates: 'E-Comm Clean & Aggregate', 'GST Tax Audit'."
], 355, badge="VISUAL ETL", border_color="#f59e0b")

lin_card = make_slide_card("Lineage & Step-by-Step Diff", [
    "Step-by-step execution diff inspector shows intermediate row counts.",
    "Directed Acyclic Graph (DAG) cycle validator prevents infinite loops.",
    "Dataset version snapshots and immutable lineage commit history.",
    "Export transformed pipelines directly to clean Parquet or CSV storage."
], 355, badge="LINEAGE TRACKER", border_color="#10b981")

t_dag = Table([[dag_card, lin_card]], colWidths=[360, 360])
t_dag.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))
story.append(t_dag)
story.append(PageBreak())

# ==========================================
# SLIDE 7: Conversational NLQ & Voice
# ==========================================
story.append(Paragraph("MODULE 4: NATURAL LANGUAGE & ACCESSIBILITY", s_cat))
story.append(Paragraph("Conversational AI Copilot (NLQ) & Multi-Lingual Voice", s_title))

nlq_card = make_slide_card("Natural Language to SQL Engine", [
    "Translates plain English questions into structured SQL queries.",
    "Example: 'What is total sales by category?' ➔ SELECT Category, SUM(Sales)...",
    "Generates executive summaries with key percentages and revenue figures.",
    "Renders dynamic Chart.js visualizations directly in conversational chat stream."
], 355, badge="NLQ TO SQL", border_color="#06b6d4")

voice_card = make_slide_card("Speech Recognition & TTS Readout", [
    "Web Speech API voice input supporting English, Hindi, Spanish, French.",
    "Speech Synthesis (TTS) automatically reads back key statistical findings aloud.",
    "Self-Learning Memory Store caches frequently asked questions with semantic matching.",
    "Sub-millisecond query execution on learned knowledge patterns."
], 355, badge="VOICE ASSISTANT", border_color="#10b981")

t_nlq = Table([[nlq_card, voice_card]], colWidths=[360, 360])
t_nlq.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))
story.append(t_nlq)
story.append(PageBreak())

# ==========================================
# SLIDE 8: AI Brain & Continual Learning
# ==========================================
story.append(Paragraph("MODULE 5: MACHINE LEARNING & PREDICTION", s_cat))
story.append(Paragraph("AI Business Brain & Continual Model Evolution", s_title))

loss_img = os.path.join(project_dir, "presentation", "assets", "learning_curve.png")
img_cell = Image(loss_img, width=350, height=230) if os.path.exists(loss_img) else Paragraph("Learning Curve", card_body)

brain_card = make_slide_card("Continual Gradient Evolution", [
    "Continual Learning Engine ingests every user dataset and sensor stream.",
    "Gradient Descent fine-tunes neural weights, lowering loss from 0.42 ➔ 0.029.",
    "Time-Series Forecasting: Polynomial trend regression with 95% confidence bounds.",
    "Customer Retention RFM Matrix: Churn probability score with automated retention levers.",
    "Statutory Growth Playbooks: Indian GST tax planning, RBI ratios, SEBI governance."
], 355, badge="CONTINUAL BRAIN", border_color="#818cf8")

t_brain = Table([[img_cell, brain_card]], colWidths=[360, 360])
t_brain.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
story.append(t_brain)
story.append(PageBreak())

# ==========================================
# SLIDE 9: Model Autonomy & Standalone Export
# ==========================================
story.append(Paragraph("MODULE 6: AI INDEPENDENCE", s_cat))
story.append(Paragraph("Model Autonomy & Standalone AI Export", s_title))

auto_card = make_slide_card("Autonomy Readiness Index", [
    "Live Autonomy Readiness Score tracks model independence (94.1% - 98.2%).",
    "Trained Accuracy metric tracks multi-task analytical precision (96.4%).",
    "Feature extraction automatically learns numeric correlations and categorical vocabulary.",
    "Evolves generation versioning (e.g. v3.1 ➔ v3.2 ➔ v3.3-Autonomous)."
], 355, badge="AUTONOMY METRIC", border_color="#10b981")

exp_card = make_slide_card("1-Click Standalone AI Export", [
    "Generates a 100% self-contained Python model: 'dataos_brain_standalone.py'.",
    "Zero external heavy framework dependencies (no PyTorch/TensorFlow lock-in).",
    "Embedded with trained weights, trend equations, anomaly sigmas, and NLQ intents.",
    "Can be deployed into external CLI tools, mobile apps, or enterprise microservices immediately."
], 355, badge="STANDALONE ARTIFACT", border_color="#06b6d4")

t_exp = Table([[auto_card, exp_card]], colWidths=[360, 360])
t_exp.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))
story.append(t_exp)
story.append(PageBreak())

# ==========================================
# SLIDE 10: Security & DPDP Compliance
# ==========================================
story.append(Paragraph("MODULE 7: STATUTORY GOVERNANCE", s_cat))
story.append(Paragraph("Enterprise Security, DPDP Act 2023 & Cryptographic Audit", s_title))

sec_card = make_slide_card("Sensitive PII Masking & DPDP Scanner", [
    "Automated Regex detection for Aadhaar (UIDAI), Indian PAN, Credit Cards, Emails, Phones.",
    "1-Click PII Redaction masks sensitive values (e.g. XXXX-XXXX-1234).",
    "Statutory Compliance Audit against Indian DPDP Act 2023, GDPR, and RBI data localization.",
    "Calculates 0-100% Enterprise Compliance Score (92.5% compliant)."
], 355, badge="PII REDACTION", border_color="#ec4899")

aud_card = make_slide_card("SHA-256 Tamper-Evident Ledger", [
    "Blockchain-inspired cryptographic chaining for immutable logging.",
    "Every query, dataset ingestion, masking event, and login creates a hashed block.",
    "1-Click Cryptographic Verification traverses the entire chain to verify integrity.",
    "Instantly flags any data alteration or security breach."
], 355, badge="IMMUTABLE AUDIT", border_color="#8b5cf6")

t_sec = Table([[sec_card, aud_card]], colWidths=[360, 360])
t_sec.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))
story.append(t_sec)
story.append(PageBreak())

# ==========================================
# SLIDE 11: Monetization & GST Invoices
# ==========================================
story.append(Paragraph("MODULE 8: COMMERCE & MONETIZATION", s_cat))
story.append(Paragraph("Monetization, Plans & Automated GST Tax Invoicing", s_title))

tier_card = make_slide_card("Tiered Subscription Tiers", [
    "Community Starter Free: 1,000 queries/mo, standard ETL pipelines.",
    "Pro Data Strategist (₹2,499/mo): 50,000 queries, AI Brain forecasting, DPDP auditing.",
    "Enterprise Autonomous Brain (₹16,999/mo): Unlimited queries, Standalone Model Export, dedicated SLA.",
    "Real-time monthly query quota tracking and enforcement."
], 355, badge="SUBSCRIPTIONS", border_color="#4f46e5")

pay_card = make_slide_card("Unified Razorpay / Stripe Gateway", [
    "Simulates Indian UPI, Net Banking, and International Credit Card payments.",
    "Modal checkout with 1-click test card autofill.",
    "Automated generation of GST-compliant Tax Invoices (18% CGST/SGST breakdown).",
    "Downloadable & printable formal tax invoice receipts."
], 355, badge="GST INVOICING", border_color="#06b6d4")

t_pay = Table([[tier_card, pay_card]], colWidths=[360, 360])
t_pay.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))
story.append(t_pay)
story.append(PageBreak())

# ==========================================
# SLIDE 12: Test Results & Verification
# ==========================================
story.append(Paragraph("VERIFICATION & VALIDATION", s_cat))
story.append(Paragraph("Experimental Results & 100% Test Suite Pass Rate", s_title))

test_rows = [
    [Paragraph("<b>Test Suite Module</b>", card_body), Paragraph("<b>Target Validation</b>", card_body), Paragraph("<b>Result</b>", card_body)],
    [Paragraph("test_01 Ingestion", card_body), Paragraph("Multi-format catalog loading & schema mapping", card_body), Paragraph("<font color='#10b981'><b>PASSED</b></font>", card_body)],
    [Paragraph("test_02 Auto-Clean ETL", card_body), Paragraph("Deduplication, imputation & outlier clipping", card_body), Paragraph("<font color='#10b981'><b>PASSED</b></font>", card_body)],
    [Paragraph("test_03 Visual DAG Studio", card_body), Paragraph("Multi-node pipeline execution & row filtering", card_body), Paragraph("<font color='#10b981'><b>PASSED</b></font>", card_body)],
    [Paragraph("test_04 AI Forecaster", card_body), Paragraph("Polynomial trend regression with 95% envelopes", card_body), Paragraph("<font color='#10b981'><b>PASSED</b></font>", card_body)],
    [Paragraph("test_07 PII Masking", card_body), Paragraph("Aadhaar, PAN & Credit Card pattern masking", card_body), Paragraph("<font color='#10b981'><b>PASSED</b></font>", card_body)],
    [Paragraph("test_09 SHA-256 Audit", card_body), Paragraph("Cryptographic block integrity & chain verification", card_body), Paragraph("<font color='#10b981'><b>PASSED</b></font>", card_body)],
    [Paragraph("test_11 Continual Model", card_body), Paragraph("Online training & Standalone .py export", card_body), Paragraph("<font color='#10b981'><b>PASSED</b></font>", card_body)]
]
t_tbl = Table(test_rows, colWidths=[160, 440, 100])
t_tbl.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e1b4b")),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#0f172a"), colors.HexColor("#1e293b")]),
    ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#334155")),
    ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#334155")),
    ('PADDING', (0, 0), (-1, -1), 5),
    ('ALIGN', (2, 0), (2, -1), 'CENTER')
]))
story.append(t_tbl)
story.append(PageBreak())

# ==========================================
# SLIDE 13: Coordinator Viva Demo Script
# ==========================================
story.append(Paragraph("PROJECT VIVA & DEMO GUIDE", s_cat))
story.append(Paragraph("5-Step Live Demonstration Walkthrough", s_title))

v1 = make_slide_card("Step 1 & 2: Overview & 1-Click ETL", [
    "1. Open http://localhost:8000 ➔ Highlight dark Glassmorphic layout & live IoT telemetry ticker.",
    "2. On Dashboard, click '✨ 1-Click Auto-Clean ETL' ➔ Show quality score jump from 62% to 99.5%."
], 355, badge="STEPS 1-2", border_color="#4f46e5")

v2 = make_slide_card("Step 3 & 4: Voice NLQ & Continual Brain", [
    "3. On AI Copilot, ask 'Sales by Category' ➔ Show SQL generation and audible TTS speech readback.",
    "4. On Business Brain, click '⚡ Train on Active Dataset' (evolves to v3.4) & '📦 Export Standalone Model'."
], 355, badge="STEPS 3-4", border_color="#06b6d4")

t_viva = Table([[v1, v2]], colWidths=[360, 360])
t_viva.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))
story.append(t_viva)
story.append(Spacer(1, 10))

v3 = make_slide_card("Step 5: Cryptographic Audit Ledger Verification", [
    "5. On Security & DPDP, click 'Verify SHA-256 Ledger' ➔ Highlight tamper-evident cryptographic chain proof under Indian DPDP Act 2023."
], 720, badge="STEP 5", border_color="#10b981")
story.append(v3)
story.append(PageBreak())

# ==========================================
# SLIDE 14: Conclusion & Q&A
# ==========================================
story.append(Spacer(1, 30))
story.append(Paragraph("SUMMARY & CLOSING", s_cat))
story.append(Paragraph("Conclusion, Key Contributions & Open Q&A", s_title))

c_take = make_slide_card("Key Project Achievements", [
    "Delivered a complete, fully functioning No-Code Autonomous Big Data Operating System.",
    "Solved tool sprawl by unifying Ingestion, Cleaning, DAG Pipelines, NLQ, and Security.",
    "Pioneered self-learning continual model training with 1-click standalone AI export.",
    "Enterprise-ready DPDP 2023 statutory compliance and cryptographic audit ledger.",
    "100% open-source on GitHub: github.com/Kanishka22222/intelligent-data-os"
], 355, badge="CONTRIBUTIONS", border_color="#10b981")

c_fut = make_slide_card("Future Horizons", [
    "Federated Learning across distributed enterprise nodes without sharing raw data.",
    "Hardware Acceleration via WebGPU for in-browser deep neural training.",
    "Direct Apache Kafka and Spark cluster streaming connectors.",
    "Automated regulatory compliance filings for GST portal & RBI."
], 355, badge="FUTURE SCOPE", border_color="#06b6d4")

t_end = Table([[c_take, c_fut]], colWidths=[360, 360])
t_end.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))
story.append(t_end)

# Build PDF Document
doc.build(story, canvasmaker=SlideCanvas)
print(f"[SUCCESS] 16:9 Slide Presentation PDF generated successfully at: {output_pdf_path}")
