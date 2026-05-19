import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ================ CONFIGURAÇÃO DA PÁGINA =================
st.set_page_config(
    page_title = "Etiquetas IAC/PAQLF",
    layout = "centered"
)

# =============== SELEÇÕES ===============================
ensaio = st.selectbox(
    "Qual etiqueta deseja gerar? (IAC ou PAQLF)",
    ["IAC", "PAQLF"]
)

st.text_input(
    "Qual o valor?",
    placeholder = "Ex: 686"
)

# ============= FUNÇÕES =================================
cm = 28.3465
largura_etiqueta = 10 * cm
altura_etiqueta = 1.5 * cm
largura_coluna = largura_etiqueta / 4

def desenhar_pagina(c, valor, numeros, ensaio):

    for idx, num in enumerate(numeros):
        x_centro = (idx * largura_coluna) + (largura_coluna / 2)
        y_centro = altura_etiqueta / 2

        linha1 = f"{ensaio}"
        linha2 = f"{valor}"

        c.setFont(times_negrito, 10)
        c.drawCentredString(x_centro, y_centro + 2.5, linha1)

        c.setFont(times_negrito, 10)
        c.drawCentredString(x_centro, y_centro - 2.5, linha2)

        c.setFont(times_negrito, 12)
    
    c.showPage()

def gerar_pdf()