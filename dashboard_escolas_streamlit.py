import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
df = pd.read_csv("dashboard_escolas_guaraciaba.csv")

# Configurar a página
st.set_page_config(
    page_title="Painel de Gestão Educacional",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paleta de cores
COR_PRINCIPAL = "#007BFF"
COR_BACKGROUND_CARD = "#E9F2FA"

# Estilização personalizada
st.markdown(f"""
    <style>
        .block-container {{
            padding-top: 2rem;
        }}
        .stMetric > div > div:first-child {{
            color: {COR_PRINCIPAL};
        }}
        .metric-container {{
            background-color: {COR_BACKGROUND_CARD};
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        .metric-value {{
            font-size: 36px;
            font-weight: bold;
            color: {COR_PRINCIPAL};
        }}
        .metric-label {{
            font-size: 16px;
        }}
    </style>
""", unsafe_allow_html=True)

# Sidebar - Filtros
st.sidebar.header("🔍 Filtros")
zona = st.sidebar.multiselect("Zona", options=df["localizacao"].unique(), default=df["localizacao"].unique())
categoria = st.sidebar.multiselect("Categoria", options=df["categoria_administrativa"].unique(), default=df["categoria_administrativa"].unique())
porte = st.sidebar.multiselect("Porte", options=df["porte"].unique(), default=df["porte"].unique())

# Aplicar filtros
df_filtrado = df[
    df["localizacao"].isin(zona) &
    df["categoria_administrativa"].isin(categoria) &
    df["porte"].isin(porte)
]

# Cabeçalho
st.markdown(f"""
    <h1 style='color: {COR_PRINCIPAL}'>📊 Painel de Gestão Educacional</h1>
    <p style='font-size: 16px;'>Indicadores das escolas de Guaraciaba do Norte (CE) — Base: Censo Escolar 2024</p>
    <hr style='margin-top: 0;'>
""", unsafe_allow_html=True)

# Métricas
col1, col2, col3 = st.columns(3)

col1.markdown(f"""
    <div class='metric-container'>
        <div class='metric-label'>Total de Escolas</div>
        <div class='metric-value'>{len(df_filtrado)}</div>
    </div>
""", unsafe_allow_html=True)

perc_privadas = df_filtrado[df_filtrado["categoria_administrativa"] == "Privada"].shape[0] / len(df_filtrado) * 100 if len(df_filtrado) > 0 else 0
col2.markdown(f"""
    <div class='metric-container'>
        <div class='metric-label'>% Escolas Privadas</div>
        <div class='metric-value'>{perc_privadas:.1f}%</div>
    </div>
""", unsafe_allow_html=True)

perc_urbana = df_filtrado[df_filtrado["localizacao"] == "Urbana"].shape[0] / len(df_filtrado) * 100 if len(df_filtrado) > 0 else 0
col3.markdown(f"""
    <div class='metric-container'>
        <div class='metric-label'>% Escolas em Zona Urbana</div>
        <div class='metric-value'>{perc_urbana:.1f}%</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Gráfico: Categoria Administrativa
st.subheader("🏡 Categoria Administrativa")
categoria_fig = px.pie(
    df_filtrado,
    names="categoria_administrativa",
    title="Distribuição: Pública vs Privada",
    color_discrete_sequence=px.colors.sequential.Blues,
    hole=0.4
)
categoria_fig.update_traces(textinfo="percent+label")
st.plotly_chart(categoria_fig, use_container_width=True)

# Novos gráficos podem ser adicionados aqui
