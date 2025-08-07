import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(layout="wide", page_title="Painel Educacional - Guaraciaba do Norte")

# Carregamento dos dados
@st.cache_data
def carregar_dados():
    return pd.read_csv("dashboard_escolas_guaraciaba.csv")

df = carregar_dados()

# Título
st.markdown("""
    <h1 style='text-align: center; color: #2E86C1;'>📊 Painel Educacional — Guaraciaba do Norte (CE)</h1>
    <br>
""", unsafe_allow_html=True)

# Filtros laterais
with st.sidebar:
    st.sidebar.title("🔎 Filtros")
    categoria = st.selectbox("Categoria", options=["Todas"] + sorted(df["categoria_administrativa"].dropna().unique()))
    zona = st.selectbox("Zona", options=["Todas"] + sorted(df["localizacao"].dropna().unique()))
    porte = st.selectbox("Porte", options=["Todas"] + sorted(df["porte"].dropna().unique()))

# Aplicar filtros
df_filtrado = df.copy()
if categoria != "Todas":
    df_filtrado = df_filtrado[df_filtrado["categoria_administrativa"] == categoria]
if zona != "Todas":
    df_filtrado = df_filtrado[df_filtrado["localizacao"] == zona]
if porte != "Todas":
    df_filtrado = df_filtrado[df_filtrado["porte"] == porte]

# Indicadores principais
col1, col2, col3 = st.columns(3)
col1.metric("Total de Escolas", len(df_filtrado))
col2.metric("% Públicas", f"{(df_filtrado['categoria_administrativa'].str.contains('Pública', na=False).mean() * 100):.1f}%")
col3.metric("% Urbanas", f"{(df_filtrado['localizacao'].str.contains('Urbana', na=False).mean() * 100):.1f}%")

# Filtrar apenas escolas municipais
df_municipais = df_filtrado[df_filtrado['dependencia_administrativa'].str.lower() == 'municipal']

# Métricas específicas para escolas municipais
total_escolas = len(df_filtrado)
total_municipais = len(df_municipais)
perc_municipais = (total_municipais / total_escolas) * 100 if total_escolas > 0 else 0
perc_urbana_municipal = (df_municipais['localizacao'] == 'Urbana').mean() * 100 if total_municipais > 0 else 0
perc_rural_municipal = (df_municipais['localizacao'] == 'Rural').mean() * 100 if total_municipais > 0 else 0

# Cards com destaque para municipais
st.markdown("### 🏫 Destaques das Escolas Municipais")
col4, col5, col6 = st.columns(3)
col4.metric("Qtd Escolas Municipais", total_municipais)
col5.metric("% Municipais na Zona Urbana", f"{perc_urbana_municipal:.1f}%")
col6.metric("% Municipais na Zona Rural", f"{perc_rural_municipal:.1f}%")

st.markdown("---")

# Gráficos
col7, col8 = st.columns(2)

with col7:
    fig1 = px.histogram(df_filtrado, x="categoria_administrativa", color="categoria_administrativa",
                        title="Distribuição por Categoria")
    st.plotly_chart(fig1, use_container_width=True)

with col8:
    fig2 = px.histogram(df_filtrado, x="localizacao", color="localizacao",
                        title="Distribuição por Zona")
    st.plotly_chart(fig2, use_container_width=True)

col9, col10 = st.columns(2)

with col9:
    fig3 = px.histogram(df_filtrado, x="porte", color="porte",
                        title="Distribuição por Porte")
    st.plotly_chart(fig3, use_container_width=True)

with col10:
    etapas = df_filtrado["etapas_modalidades_oferecidas"].dropna().str.split(", ").explode()
    fig4 = px.histogram(etapas, x=etapas, color=etapas,
                        title="Distribuição por Etapas de Ensino")
    st.plotly_chart(fig4, use_container_width=True)

# Tabela final
st.markdown("""
    <br><h3 style='text-align: left; color: #2E86C1;'>📋 Detalhamento das Escolas</h3>
""", unsafe_allow_html=True)
st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True)
