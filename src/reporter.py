import datetime
from fpdf import FPDF

# ==========================================
# 1. CORPORATE PDF STYLING TEMPLATE
# ==========================================

class CorporatePDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        watermark_text = f"CONFIDENTIAL // ACIS INTELLIGENCE ENGINE V2 // GENERATED: {timestamp}"
        
        self.cell(0, 10, watermark_text, align="R")
        self.ln(8)
        
        self.set_draw_color(200, 200, 200)
        self.line(15, self.get_y(), 195, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_draw_color(200, 200, 200)
        self.line(15, self.get_y(), 195, self.get_y())
        
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()} of {{nb}}", align="C")

# ==========================================
# 2. DOCUMENT COMPILATION ENGINE
# ==========================================

def generate_pdf_report(markdown_text: str, topic: str, filename: str = "Corporate_Intelligence_Brief.pdf") -> str:
    pdf = CorporatePDF(orientation="P", unit="mm", format="A4")
    pdf.alias_nb_pages() 
    pdf.set_margins(left=15, top=15, right=15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # ----------------------------------------
    # THE EXECUTIVE HEADER CARD
    # ----------------------------------------
    pdf.set_fill_color(230, 240, 255)
    pdf.set_draw_color(70, 130, 180)
    pdf.set_line_width(0.5)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(0, 0, 128)
    
    title_text = f"INTELLIGENCE DIRECTIVE:\n{topic.upper()}"
    pdf.multi_cell(0, 10, txt=title_text, border=1, align="C", fill=True)
    pdf.ln(10)
    
    # ----------------------------------------
    # THE TEXT BODY (DEFENSIVE PARSER)
    # ----------------------------------------
    cleaned_lines = markdown_text.split("\n")
    for line in cleaned_lines:
        line = line.replace("**", "")
        
        # DEFENSE 1: Skip raw markdown table separators that break PDF boundaries
        if "|---" in line or line.startswith("---") or line.startswith("==="):
            continue 
            
        if line.startswith("#"):
            clean_heading = line.replace("#", "").strip()
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(65, 105, 225) 
            try:
                pdf.multi_cell(0, 8, txt=clean_heading)
            except Exception:
                pass # Fail silently instead of crashing
            pdf.ln(2)
        else:
            if not line.strip():
                pdf.ln(3)
                continue
                
            pdf.set_font("Helvetica", "", 11)
            pdf.set_text_color(50, 50, 50) 
            
            safe_text = line.encode('latin-1', 'replace').decode('latin-1')
            
            # DEFENSE 2: Try-Except block for unbroken strings (like massive URLs)
            try:
                pdf.multi_cell(0, 6, txt=safe_text)
            except Exception:
                # If it still crashes, forcefully truncate the string so the app survives
                try:
                    pdf.multi_cell(0, 6, txt=safe_text[:90] + "... [Text truncated for PDF safety]")
                except Exception:
                    pass
            
    pdf.output(filename)
    return filename