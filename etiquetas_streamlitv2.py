import streamlit as st
import pandas as pd
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

.titulo-app {
    font-size: 38px;
    font-weight: 700;
    color: #0F172A;
}

.subtitulo-app {
    font-size: 18px;
    color: #475569;
    margin-bottom: 25px;
}

.card {
    background-color: white;
    padding: 25px;
    border-radius: 16px;
    border: 1px solid #E2E8F0;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 20px;
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

.stMultiSelect div[data-baseweb="select"] {
    background-color: #F8FAFC;
    border-radius: 10px;
    border: 1px solid #CBD5E1;
}

.stMultiSelect span[data-baseweb="tag"] {
    background-color: #166534 !important;
    color: white !important;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ================= CABEÇALHO =================
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
        Gerador de Etiquetas ATVOS
    </div>

    <div class="subtitulo-app">
        Laboratório Químico • Agrorobótica
    </div>
    """,
    unsafe_allow_html=True
)

# ================= FONTES =================
try:
    pdfmetrics.registerFont(TTFont("TimesNewRoman", r"C:\Windows\Fonts\times.ttf"))
    pdfmetrics.registerFont(TTFont("TimesNewRomanBold", r"C:\Windows\Fonts\timesbd.ttf"))

    FONTE_NORMAL = "TimesNewRoman"
    FONTE_NEGRITO = "TimesNewRomanBold"

except:
    FONTE_NORMAL = "Times-Roman"
    FONTE_NEGRITO = "Times-Bold"

# ================= CONFIGURAÇÕES DAS ETIQUETAS =================
cm = 28.3465
largura_etiqueta = 10 * cm
altura_etiqueta = 1.5 * cm
largura_coluna = largura_etiqueta / 4

# ================= FORMULÁRIO =================

arquivo_excel = st.file_uploader(
    "1.Carregue o arquivo Excel com as etiquetas virtuais",
    type=["xlsx"]
)

opcoes_legendas = {
    "k": "KP Mehlich",
    "m": "Macro",
    "u": "Micro",
    "s": "Enxofre",
    "p": "pH",
    "c": "MO",
    "t": "Textura",
    "r": "P Resina"
}

selecionadas = st.multiselect(
    "3.Selecione as análises",
    options=list(opcoes_legendas.keys()),
    default=["m", "s", "r", "p", "c"],
    format_func=lambda x: f"{x} - {opcoes_legendas[x]}"
)

# ================= FUNÇÕES =================
def limpar_lista_etiquetas(df, sigla):
    valores = (
        df[sigla]
        .dropna()
        .astype(str)
        .str.strip()
        .tolist()
    )

    valores = [v for v in valores if v != "" and v.lower() != "nan"]

    return valores


def quebrar_codigo(codigo):
    partes = codigo.split("|", 1)

    analise = partes[0] if len(partes) > 0 else ""
    especif = partes[1] if len(partes) > 1 else ""

    return analise, especif


def desenhar_pagina(c, codigos):
    for idx, codigo in enumerate(codigos):
        x_centro = (idx * largura_coluna) + (largura_coluna / 2)
        y_centro = altura_etiqueta / 2

        analise, especif = quebrar_codigo(codigo)

        linha1 = analise
        linha2 = especif

        c.setFont(FONTE_NEGRITO, 10)
        c.drawCentredString(x_centro, y_centro + 5, linha1)

        c.setFont(FONTE_NEGRITO, 10)
        c.drawCentredString(x_centro, y_centro - 10, linha2)

    c.showPage()


def gerar_pdf_por_sigla(sigla, codigos, pasta_saida, nome_arquivo):
    if not codigos:
        return None

    nome_base = Path(nome_arquivo).stem
    nome_pdf = f"{nome_base}_{sigla}.pdf"
    output_path = pasta_saida / nome_pdf

    c = canvas.Canvas(
        str(output_path),
        pagesize=(largura_etiqueta, altura_etiqueta)
    )

    for i in range(0, len(codigos), 4):
        grupo = codigos[i:i + 4]
        desenhar_pagina(c, grupo)

    c.save()

    return output_path


# ================= BOTÃO =================
if st.button("Gerar etiquetas"):

    if arquivo_excel is None:
        st.error("[ERRO]: Carregue o arquivo Excel.")

    elif not selecionadas:
        st.error("[ERRO]: Selecione pelo menos uma análise.")

    else:
        df = pd.read_excel(arquivo_excel)

        colunas_existentes = list(df.columns)

        selecionadas_validas = [
            sigla for sigla in selecionadas
            if sigla in colunas_existentes
        ]

        if not selecionadas_validas:
            st.error("[ERRO]: Nenhuma análise selecionada existe no arquivo Excel.")

        else:
            with tempfile.TemporaryDirectory() as tmpdir:
                pasta_saida = Path(tmpdir)
                arquivos = []

                for sigla in selecionadas_validas:
                    codigos = limpar_lista_etiquetas(df, sigla)

                    pdf = gerar_pdf_por_sigla(
                        sigla=sigla,
                        codigos=codigos,
                        pasta_saida=pasta_saida,
                        nome_arquivo=arquivo_excel.name
                    )

                    if pdf is not None:
                        arquivos.append(pdf)
                        
                zip_path = pasta_saida / "Etiquetas_ATVOS.zip"

                with zipfile.ZipFile(zip_path, "w") as zipf:
                    for arquivo in arquivos:
                        zipf.write(arquivo, arcname=arquivo.name)

                with open(zip_path, "rb") as f:
                    st.success("Etiquetas geradas com sucesso!")

                    st.download_button(
                        label="Baixar etiquetas em ZIP",
                        data=f,
                        file_name="Etiquetas_Quimico.zip",
                        mime="application/zip"
                    )

st.markdown('</div>', unsafe_allow_html=True)