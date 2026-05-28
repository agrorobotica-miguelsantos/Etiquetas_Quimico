import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
import tempfile

# ================ CONFIGURAÇÃO DA PÁGINA =================
st.set_page_config(
    page_title="Etiquetas IAC/PAQLF",
    layout="centered"
)

st.markdown(
    """
    <style>
    .titulo-app {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .subtitulo-app {
        text-align: center;
        font-size: 18px;
        color: #666666;
    }
    </style>

    <div class="titulo-app">
        Gerador de Etiquetas IAC/PAQLF
    </div>

    <div class="subtitulo-app">
        Laboratório Químico • Agrorobótica
    </div>
    """,
    unsafe_allow_html=True
)

# ================ FONTES =================
try:
    pdfmetrics.registerFont(TTFont("TimesNewRoman", r"C:\Windows\Fonts\times.ttf"))
    pdfmetrics.registerFont(TTFont("TimesNewRomanBold", r"C:\Windows\Fonts\timesbd.ttf"))

    times_negrito = "TimesNewRomanBold"

except:
    times_negrito = "Times-Bold"

# ================ CONFIGURAÇÕES =================
cm = 28.3465
largura_etiqueta = 10 * cm
altura_etiqueta = 1.5 * cm
largura_coluna = largura_etiqueta / 4

# ================ INPUTS =================
ensaio = st.selectbox(
    "Qual etiqueta deseja gerar?",
    ["IAC", "PAQLF"]
)

valor = st.text_input(
    "Qual o valor?",
    placeholder="Ex: 686"
)

quantidade = st.number_input(
    "Quantidade de etiquetas",
    min_value=1,
    value=20,
    step=1
)

# ============= FUNÇÕES =================
def desenhar_pagina(c, valor, quantidade_grupo, ensaio):
    for idx in range(quantidade_grupo):
        x_centro = (idx * largura_coluna) + (largura_coluna / 2)
        y_centro = altura_etiqueta / 2

        linha1 = f"{ensaio}"
        linha2 = f"{valor}"

        c.setFont(times_negrito, 12)
        c.drawCentredString(x_centro, y_centro + 5, linha1)

        c.setFont(times_negrito, 12)
        c.drawCentredString(x_centro, y_centro - 8, linha2)

    c.showPage()


def gerar_pdf(ensaio, valor, quantidade, pasta_saida):
    nome_pdf = f"Etiquetas_{ensaio}_{valor}.pdf"
    output_path = pasta_saida / nome_pdf

    c = canvas.Canvas(
        str(output_path),
        pagesize=(largura_etiqueta, altura_etiqueta)
    )

    restantes = quantidade

    while restantes > 0:
        qtd_pagina = min(4, restantes)

        desenhar_pagina(
            c,
            valor,
            qtd_pagina,
            ensaio
        )

        restantes -= qtd_pagina

    c.save()

    return output_path


# ================ BOTÃO =================
if st.button("Gerar etiquetas"):

    if not valor:
        st.error("[ERRO]: Informe o valor.")

    else:
        with tempfile.TemporaryDirectory() as tmpdir:
            pasta_saida = Path(tmpdir)

            pdf = gerar_pdf(
                ensaio=ensaio,
                valor=valor,
                quantidade=quantidade,
                pasta_saida=pasta_saida
            )

            with open(pdf, "rb") as f:
                st.success("Etiquetas geradas com sucesso!")

                st.download_button(
                    label="Baixar PDF",
                    data=f,
                    file_name=pdf.name,
                    mime="application/pdf"
                )