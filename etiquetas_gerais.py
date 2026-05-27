from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Fonte
pdfmetrics.registerFont(TTFont('TimesNewRomanBold', r'C:\Windows\Fonts\timesbd.ttf'))

# ===== CONFIG =====
cm = 28.3465
largura_etiqueta = 10 * cm
altura_etiqueta = 1.5 * cm

output_path = r"C:\Users\MiguelSantos\OneDrive - Agrorobotica Fotonica Em Certificacoes Agroambientais\AGROROBOTICA\PROJETOS\Etiquetas_Quimico\Etiquetas_Gerais"

if not output_path.lower().endswith(".pdf"):
    output_path += ".pdf"

pasta = os.path.dirname(output_path)
if pasta and not os.path.exists(pasta):
    os.makedirs(pasta)

c = canvas.Canvas(output_path, pagesize=(largura_etiqueta, altura_etiqueta))
largura_coluna = largura_etiqueta / 4

# ===== DESENHO =====
def desenhar_pagina():
    for idx in range(4):
        x_centro = (idx * largura_coluna) + (largura_coluna / 2)
        y_centro = altura_etiqueta / 2

        linha1 = f"BRANCO"
        linha2 = f"/         /"

        c.setFont("TimesNewRomanBold", 10)
        c.drawCentredString(x_centro, y_centro + 6, linha1)

        c.setFont("TimesNewRomanBold", 10)
        c.drawCentredString(x_centro, y_centro - 12, linha2)

    c.showPage()
    c.save()

# ===== GERAÇÃO =====
desenhar_pagina()