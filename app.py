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
    categoria = st.selectbox("Categoria", options=["Todas"] + sorted(df["Categoria"].dropna().unique().tolist()))
    zona = st.selectbox("Zona", options=["Todas"] + sorted(df["Zona"].dropna().unique().tolist()))
    porte = st.selectbox("Porte", options=["Todas"] + sorted(df["Porte"].dropna().unique().tolist()))

# Aplicar filtros
if categoria != "Todas":
    df = df[df["Categoria"] == categoria]
if zona != "Todas":
    df = df[df["Zona"] == zona]
if porte != "Todas":
    df = df[df["Porte"] == porte]

# Linhas divididas para layout em colunas
col1, col2, col3 = st.columns(3)

# Indicadores principais
col1.metric("Total de Escolas", len(df))
col2.metric("% Públicas", f"{(df['Categoria'].value_counts(normalize=True).get('Pública', 0)*100):.1f}%")
col3.metric("% Urbanas", f"{(df['Zona'].value_counts(normalize=True).get('Urbana', 0)*100):.1f}%")

# Filtrar apenas escolas municipais
df_municipais = df[df['Categoria'] == 'Municipal']

# Métricas específicas para escolas municipais
total_escolas = len(df)
total_municipais = len(df_municipais)
perc_municipais = (total_municipais / total_escolas) * 100 if total_escolas > 0 else 0
perc_urbana_municipal = (df_municipais['Zona'] == 'Urbana').mean() * 100 if total_municipais > 0 else 0
perc_rural_municipal = (df_municipais['Zona'] == 'Rural').mean() * 100 if total_municipais > 0 else 0

# Cards com destaque para municipais
st.markdown("### 🏫 Destaques das Escolas Municipais")
col4, col5, col6 = st.columns(3)
col4.metric("Qtd Escolas Municipais", total_municipais)
col5.metric("% Municipais na Zona Urbana", f"{perc_urbana_municipal:.1f}%")
col6.metric("% Municipais na Zona Rural", f"{perc_rural_municipal:.1f}%")


st.markdown("---")

# Gráficos
col4, col5 = st.columns(2)

with col4:
    fig1 = px.histogram(df, x="Categoria", color="Categoria",
                        title="Distribuição por Categoria")
    st.plotly_chart(fig1, use_container_width=True)

with col5:
    fig2 = px.histogram(df, x="Zona", color="Zona",
                        title="Distribuição por Zona")
    st.plotly_chart(fig2, use_container_width=True)

col6, col7 = st.columns(2)

with col6:
    fig3 = px.histogram(df, x="Porte", color="Porte",
                        title="Distribuição por Porte")
    st.plotly_chart(fig3, use_container_width=True)

with col7:
    etapas = df["Etapas"].dropna().str.split(", ").explode()
    fig4 = px.histogram(etapas, x=etapas, color=etapas,
                        title="Distribuição por Etapas de Ensino")
    st.plotly_chart(fig4, use_container_width=True)

# Tabela de dados
st.markdown("""
    <br><h3 style='text-align: left; color: #2E86C1;'>📋 Detalhamento das Escolas</h3>
""", unsafe_allow_html=True)

st.dataframe(df, use_container_width=True)
