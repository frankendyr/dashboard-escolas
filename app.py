import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(layout="wide", page_title="Painel Educacional - Guaraciaba do Norte")

# Função para carregar os dados
@st.cache_data
def carregar_dados():
    return pd.read_csv("dashboard_escolas_guaraciaba.csv")

df = carregar_dados()

# Renomear colunas para facilitar o uso interno
df = df.rename(columns={
    "localizacao": "Zona",
    "categoria_administrativa": "Categoria",
    "porte": "Porte",
    "etapas_modalidades_oferecidas": "Etapas",
    "dependencia_administrativa": "Dependencia"
})

# Título principal
st.markdown("""
    <h1 style='text-align: center; color: #2E86C1;'>📊 Painel Educacional — Guaraciaba do Norte (CE)</h1>
    <br>
""", unsafe_allow_html=True)

# Filtros laterais
with st.sidebar:
    st.sidebar.title("🔎 Filtros")
    categoria = st.selectbox("Categoria", options=["Todas"] + sorted(df["Categoria"].dropna().unique()))
    zona = st.selectbox("Zona", options=["Todas"] + sorted(df["Zona"].dropna().unique()))
    porte = st.selectbox("Porte", options=["Todas"] + sorted(df["Porte"].dropna().unique()))

# Aplicar filtros
df_filtrado = df.copy()
if categoria != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Categoria"] == categoria]
if zona != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Zona"] == zona]
if porte != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Porte"] == porte]

# Indicadores principais
col1, col2, col3 = st.columns(3)
col1.metric("Total de Escolas", len(df_filtrado))
col2.metric("% Públicas", f"{(df_filtrado['Categoria'].str.contains('Pública', na=False).mean() * 100):.1f}%")
col3.metric("% Urbanas", f"{(df_filtrado['Zona'].str.contains('Urbana', na=False).mean() * 100):.1f}%")

# Métricas específicas para escolas municipais
df_municipais = df_filtrado[df_filtrado['Dependencia'].str.lower() == 'municipal']

total_escolas = len(df_filtrado)
total_municipais = len(df_municipais)
perc_municipais = (total_municipais / total_escolas * 100) if total_escolas > 0 else 0
perc_urbana_municipal = (df_municipais['Zona'] == 'Urbana').mean() * 100 if total_municipais > 0 else 0
perc_rural_municipal = (df_municipais['Zona'] == 'Rural').mean() * 100 if total_municipais > 0 else 0

st.markdown("### 🏫 Destaques das Escolas Municipais")
col4, col5, col6 = st.columns(3)
col4.metric("Qtd Escolas Municipais", total_municipais)
col5.metric("% Municipais na Zona Urbana", f"{perc_urbana_municipal:.1f}%")
col6.metric("% Municipais na Zona Rural", f"{perc_rural_municipal:.1f}%")

st.markdown("---")

# Gráficos principais
col7, col8 = st.columns(2)

with col7:
    fig1 = px.histogram(df_filtrado, x="Categoria", color="Categoria",
                        title="Distribuição por Categoria")
    st.plotly_chart(fig1, use_container_width=True)

with col8:
    fig2 = px.histogram(df_filtrado, x="Zona", color="Zona",
                        title="Distribuição por Zona")
    st.plotly_chart(fig2, use_container_width=True)

col9, col10 = st.columns(2)

with col9:
    fig3 = px.histogram(df_filtrado, x="Porte", color="Porte",
                        title="Distribuição por Porte")
    st.plotly_chart(fig3, use_container_width=True)

with col10:
    etapas = df_filtrado["Etapas"].dropna().str.split(", ").explode()
    fig4 = px.histogram(etapas, x=etapas, color=etapas,
                        title="Distribuição por Etapas de Ensino")
    st.plotly_chart(fig4, use_container_width=True)

# Tabela final
st.markdown("""
    <br><h3 style='text-align: left; color: #2E86C1;'>📋 Detalhamento das Escolas</h3>
""", unsafe_allow_html=True)
st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True)
