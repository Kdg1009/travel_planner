from fpdf import FPDF
from pathlib import Path
from components.plan_data import TravelPlan

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        font_path = Path("NanumGothic.ttf")
        self.add_font("Nanum", "", str(font_path), uni=True)
        self.set_font("Nanum", size=12)

    def header(self):
        self.set_font("Nanum", size=14)
        self.cell(200, 10, txt="📍 여행 일정", ln=True, align='C')

def export_to_pdf(route: TravelPlan, user_id:str):
    static_dir = Path("static")
    static_dir.mkdir(exist_ok=True)
    filename = static_dir / f"schedule_{user_id}.pdf"

    pdf = PDF()
    pdf.add_page()

    '''
        you need to complete this code
    '''

    pdf.output(str(filename))
    return str(filename)

