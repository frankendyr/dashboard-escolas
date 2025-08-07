import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Painel Educacional – Guaraciaba do Norte (CE)",
    layout="wide"
)

# Estilo customizado para fundo branco e fonte clara
st.markdown("""
    <style>
        body {
            background-color: #ffffff;
            color: #000000;
        }
        .main {
            background-color: #ffffff;
        }
        header, footer {visibility: hidden;}
        .block-container {
            padding-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Carregando os dados
@st.cache_data

def carregar_dados():
    df = pd.read_csv("dashboard_escolas_guaraciaba.csv")
    return df

df = carregar_dados()

st.sidebar.header("🔍 Filtros")
zona = st.sidebar.multiselect("Zona", options=df["Zona"].unique(), default=df["Zona"].unique())
categoria = st.sidebar.multiselect("Categoria", options=df["Categoria"].unique(), default=df["Categoria"].unique())
porte = st.sidebar.multiselect("Porte", options=df["Porte"].unique(), default=df["Porte"].unique())
etapas = st.sidebar.multiselect("Etapas", options=df["Etapas"].unique(), default=df["Etapas"].unique())

# Aplicar filtros
df_filtros = df[
    (df["Zona"].isin(zona)) &
    (df["Categoria"].isin(categoria)) &
    (df["Porte"].isin(porte)) &
    (df["Etapas"].isin(etapas))
]

# Função para criar cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Escolas", len(df_filtros))
col2.metric("Zonas", df_filtros["Zona"].nunique())
col3.metric("Categorias", df_filtros["Categoria"].nunique())
col4.metric("Etapas", df_filtros["Etapas"].nunique())

st.markdown("---")

# Gráfico de barras por Zona
fig1 = px.histogram(df_filtros, x="Zona", color="Categoria", barmode="group",
                    title="Distribuição das Escolas por Zona e Categoria")
st.plotly_chart(fig1, use_container_width=True)

# Gráfico de barras por Etapas
fig2 = px.histogram(df_filtros, x="Etapas", color="Categoria", barmode="group",
                    title="Distribuição das Etapas por Categoria")
st.plotly_chart(fig2, use_container_width=True)

# Tabela de dados
st.markdown("### 📋 Tabela de Escolas")
st.dataframe(df_filtros, use_container_width=True, height=500)
