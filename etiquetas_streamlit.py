import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
import zipfile
import tempfile

# ================= CONFIGURAÇÃO DA PÁGINA =================
st.set_page_config(
    page_title="Gerador de Etiquetas ATVOS",
    layout="centered"
)

# ================= IDENTIDADE VISUAL =================
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

.titulo-app {
    font-size: 38px;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 0px;
}

.subtitulo-app {
    font-size: 18px;
    color: #475569;
    margin-top: 0px;
    margin-bottom: 0px;
}

.stTextInput input,
.stNumberInput input {
    border-radius: 10px;
}

.stSelectbox div[data-baseweb="select"] {
    border-radius: 10px;
}
            
.stMultiSelect span[data-baseweb="tag"] {
    background-color: #166534;
    color: white;
    border-radius: 8px;
}

.stButton > button {
    width: 100%;
    background-color: #166534;
    color: white;
    border-radius: 12px;
    border: none;
    height: 50px;
    font-size: 16px;
    font-weight: 600;
    transition: 0.3s;
}

.stButton > button:hover {
    background-color: #14532d;
    color: white;
}

.stDownloadButton > button {
    width: 100%;
    background-color: #0F172A;
    color: white;
    border-radius: 12px;
    border: none;
    height: 50px;
    font-size: 16px;
    font-weight: 600;
}

.stDownloadButton > button:hover {
    background-color: #1E293B;
    color: white;
}

.stAlert {
    border-radius: 12px;
}

hr {
    margin-top: 10px;
    margin-bottom: 25px;
}
</style>
""", unsafe_allow_html=True)

# ================= CABEÇALHO =================
st.markdown(
    """
    <div class="titulo-app">
        Gerador de Etiquetas ATVOS
    </div>

    <div class="subtitulo-app">
        Laboratório Químico • Agrorobótica
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# ================= FONTES =================
try:
    pdfmetrics.registerFont(TTFont("TimesNewRoman", r"C:\Windows\Fonts\times.ttf"))
    pdfmetrics.registerFont(TTFont("TimesNewRomanBold", r"C:\Windows\Fonts\timesbd.ttf"))

    times_normal = "TimesNewRoman"
    times_negrito = "TimesNewRomanBold"

except:

    times_normal = "Times-Roman"
    times_negrito = "Times-Bold"

# ================= CONFIGURAÇÕES =================
cm = 28.3465
largura_etiqueta = 10 * cm
altura_etiqueta = 1.5 * cm
largura_coluna = largura_etiqueta / 4

# ================= FORMULÁRIO =================
st.markdown('<div class="card">', unsafe_allow_html=True)

ordem = st.text_input(
    "Qual a OS-ATVOS?",
    placeholder="Ex: 004"
)

st.subheader("Intervalo das etiquetas")

col1, col2 = st.columns(2)

with col1:
    inicio = st.number_input(
        "Começar em",
        min_value=1,
        step=1,
        value=1
    )

with col2:
    fim = st.number_input(
        "Terminar em",
        min_value=1,
        step=1,
        value=10
    )

tipo_etiqueta = st.selectbox(
    "Qual tipo deseja gerar?",
    ["FERT", "PAV", "FERT e PAV"]
)

st.subheader("Selecione as análises")

opcoes_legendas = {
    "m": "Macro",
    "u": "Micro",
    "s": "Enxofre",
    "r": "P Resina",
    "p": "pH",
    "k": "KP Mehlich",
    "t": "Textura",
    "c": "MO"
}

selecionadas = st.multiselect(
    "Análises",
    options=list(opcoes_legendas.keys()),
    default=["m", "s", "r", "p", "c"],
    format_func=lambda x: f"{x} - {opcoes_legendas[x]}"
)

# ================= FUNÇÕES =================
def desenhar_pagina(c, tipo, sigla, numeros, ordem):
    for idx, num in enumerate(numeros):
        x_centro = (idx * largura_coluna) + (largura_coluna / 2)
        y_centro = altura_etiqueta / 2

        linha1 = f"{ordem}"
        linha2 = f"ATV {tipo}"
        linha3 = f"{sigla} {str(num).zfill(3)}"

        c.setFont(times_negrito, 10)
        c.drawCentredString(x_centro, y_centro + 6, linha1)

        c.setFont(times_negrito, 10)
        c.drawCentredString(x_centro, y_centro - 3, linha2)

        c.setFont(times_negrito, 12)
        c.drawCentredString(x_centro, y_centro - 14, linha3)

    c.showPage()


def gerar_pdf_por_sigla(tipo, inicio, fim, ordem, pasta_saida, legendas):
    arquivos_gerados = []

    numeros = list(range(inicio, fim + 1))

    for sigla, repeticoes in legendas.items():

        nome_pdf = f"OS_{ordem}-ATVOS_{sigla}_{tipo}.pdf"
        output_path = pasta_saida / nome_pdf

        c = canvas.Canvas(
            str(output_path),
            pagesize=(largura_etiqueta, altura_etiqueta)
        )

        for rep in range(repeticoes):
            for i in range(0, len(numeros), 4):
                grupo = numeros[i:i + 4]
                desenhar_pagina(c, tipo, sigla, grupo, ordem)

        c.save()
        arquivos_gerados.append(output_path)

    return arquivos_gerados


# ================= BOTÃO DE GERAÇÃO =================
if st.button("Gerar etiquetas"):

    if not ordem:
        st.error("[ERRO]: Informe a OS-ATVOS.")

    elif inicio > fim:
        st.error("[ERRO]: O número inicial não pode ser maior que o número final.")

    elif not selecionadas:
        st.error("[ERRO]: Selecione pelo menos uma análise.")

    else:
        with tempfile.TemporaryDirectory() as tmpdir:
            pasta_saida = Path(tmpdir)
            pasta_saida.mkdir(parents=True, exist_ok=True)

            legendas = {sigla: 1 for sigla in selecionadas}
            arquivos = []

            if tipo_etiqueta in ["FERT", "FERT e PAV"]:
                arquivos += gerar_pdf_por_sigla(
                    "FERT",
                    inicio,
                    fim,
                    ordem,
                    pasta_saida,
                    legendas
                )

            if tipo_etiqueta in ["PAV", "FERT e PAV"]:
                arquivos += gerar_pdf_por_sigla(
                    "PAV",
                    inicio,
                    fim,
                    ordem,
                    pasta_saida,
                    legendas
                )

            zip_path = pasta_saida / f"Etiquetas_OS_{ordem}_ATVOS.zip"

            with zipfile.ZipFile(zip_path, "w") as zipf:
                for arquivo in arquivos:
                    zipf.write(arquivo, arcname=arquivo.name)

            with open(zip_path, "rb") as f:
                st.success("Etiquetas geradas com sucesso!")

                st.download_button(
                    label="Baixar PDFs em ZIP",
                    data=f,
                    file_name=f"Etiquetas_OS_{ordem}_ATVOS.zip",
                    mime="application/zip"
                )

st.markdown('</div>', unsafe_allow_html=True)