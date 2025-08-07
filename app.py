import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Painel de Gestão Educacional")

# Função para carregar os dados
@st.cache_data
def carregar_dados():
    df = pd.read_csv("dashboard_escolas_guaraciaba.csv")
    df["etapas_modalidades_oferecidas"] = df["etapas_modalidades_oferecidas"].fillna("Não informado")
    return df

df = carregar_dados()

# 🎯 Filtros
st.sidebar.header("🔍 Filtros")

zona = st.sidebar.multiselect(
    "Zona", 
    options=df["localizacao"].unique(), 
    default=df["localizacao"].unique()
)

categoria = st.sidebar.multiselect(
    "Categoria", 
    options=df["categoria_administrativa"].unique(), 
    default=df["categoria_administrativa"].unique()
)

porte = st.sidebar.multiselect(
    "Porte", 
    options=df["porte"].unique(), 
    default=df["porte"].unique()
)

# Aplicar filtros
df_filtro = df[
    (df["localizacao"].isin(zona)) &
    (df["categoria_administrativa"].isin(categoria)) &
    (df["porte"].isin(porte))
]

# 📊 Cabeçalho
st.title("📊 Painel de Gestão Educacional")
st.markdown("Indicadores das escolas de Guaraciaba do Norte (CE) — **Base: Censo Escolar 2024**")
st.markdown("---")

# 🔢 Métricas
col1, col2, col3 = st.columns(3)
col1.metric("Total de Escolas", len(df_filtro))
col2.metric("% Escolas Privadas", f'{(df_filtro["categoria_administrativa"] == "Privada").mean()*100:.1f}%')
col3.metric("% Escolas em Zona Urbana", f'{(df_filtro["localizacao"] == "Urbana").mean()*100:.1f}%')

st.markdown("---")

# 📘 Categoria Administrativa
st.subheader("🏫 Categoria Administrativa")
fig_cat = px.pie(
    df_filtro,
    names="categoria_administrativa",
    hole=0.4,
    color_discrete_sequence=px.colors.sequential.Blues,
)
st.plotly_chart(fig_cat, use_container_width=True)

# 📚 Etapas Modalidades
st.subheader("📚 Etapas e Modalidades Oferecidas")
df_etapas = df_filtro["etapas_modalidades_oferecidas"].value_counts().reset_index()
df_etapas.columns = ["Etapa", "Total"]
fig_etapas = px.bar(
    df_etapas,
    x="Etapa",
    y="Total",
    text="Total",
    color="Etapa",
    color_discrete_sequence=px.colors.sequential.Blues,
)
fig_etapas.update_layout(showlegend=False)
st.plotly_chart(fig_etapas, use_container_width=True)
