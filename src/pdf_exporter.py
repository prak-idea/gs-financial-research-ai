"""
PDF Report Builder -- GS style using fpdf2 + Liberation Sans.
"""
import shutil
import re
from fpdf import FPDF
from datetime import datetime


def setup_fonts():
    shutil.copy(
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/tmp/Regular.ttf")
    shutil.copy(
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/tmp/Bold.ttf")


def clean(text):
    if not text: return ""
    text = str(text)
    text = re.sub(r"https?://\S+", "", text)
    text = text.replace("|", " ")
    for s, d in [("\u2014","--"),("\u2013","-"),("\u2019","'"),
                  ("\u201c",chr(34)),("\u201d",chr(34))]
        text = text.replace(s, d)
    tokens = text.split()
    broken = []
    for t in tokens:
        broken.extend([t[i:i+30] for i in range(0,len(t),30)] if len(t)>30 else [t])
    return "".join(c if ord(c)<256 else "?" for c in " ".join(broken)).strip()


class GSReport(FPDF):
    def __init__(self, ticker, company, model):
        super().__init__()
        self.ticker = ticker
        self.company = company
        self.model = model
        self.add_font("F", "",  "/tmp/Regular.ttf", uni=True)
        self.add_font("F", "B", "/tmp/Bold.ttf",    uni=True)

    def header(self):
        self.set_fill_color(0, 51, 102)
        self.rect(0, 0, 210, 11, "F")
        self.set_font("F", "B", 8)
        self.set_text_color(255, 255, 255)
        self.set_xy(10, 2)
        self.cell(130, 7, "GOLDMAN SACHS  |  " + self.company)
        self.set_text_color(0, 0, 0)
        self.ln(9)

    def footer(self):
        self.set_y(-10)
        self.set_font("F", "", 7)
        self.set_text_color(130, 130, 130)
        self.cell(0, 6, "Page " + str(self.page_no()) + "  |  " + self.model, align="C")