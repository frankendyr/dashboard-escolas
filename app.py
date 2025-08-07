
import streamlit as st
import pandas as pd

# Configurações da página
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>🏛️ Painel Educacional — Guaraciaba do Norte (CE)</h1>", unsafe_allow_html=True)

# Carregar os dados
df = pd.read_csv("dashboard_escolas_guaraciaba.csv")

# Filtros laterais
categorias = ["Todas"] + sorted(df["dependencia_administrativa"].dropna().unique())
zonas = ["Todas"] + sorted(df["localizacao"].dropna().unique())
portes = ["Todas"] + sorted(df["porte"].dropna().unique())

st.sidebar.markdown("## 🔎 Filtros")
categoria = st.sidebar.selectbox("Categoria", options=categorias)
zona = st.sidebar.selectbox("Zona", options=zonas)
porte = st.sidebar.selectbox("Porte", options=portes)

# Aplicando filtros
df_filtrado = df.copy()

if categoria != "Todas":
    df_filtrado = df_filtrado[df_filtrado["dependencia_administrativa"] == categoria]

if zona != "Todas":
    df_filtrado = df_filtrado[df_filtrado["localizacao"] == zona]

if porte != "Todas":
    df_filtrado = df_filtrado[df_filtrado["porte"] == porte]

# Indicadores principais
total_escolas = len(df_filtrado)
porcentagem_publicas = round((df_filtrado["dependencia_administrativa"].str.lower() == "municipal").mean() * 100, 1)
porcentagem_urbanas = round((df_filtrado["localizacao"].str.lower() == "urbana").mean() * 100, 1)

col1, col2, col3 = st.columns(3)
col1.metric("Total de Escolas", total_escolas)
col2.metric("% Municipais", f"{porcentagem_publicas}%")
col3.metric("% Urbanas", f"{porcentagem_urbanas}%")

# Dados adicionais sobre escolas municipais
df_municipais = df_filtrado[df_filtrado["dependencia_administrativa"].str.lower() == "municipal"]

if not df_municipais.empty:
    st.markdown("### 🏫 Detalhes das Escolas Municipais")
    st.write(f"- Total de escolas municipais: **{len(df_municipais)}**")
    st.write(f"- % do total: **{round(len(df_municipais) / total_escolas * 100, 1)}%**")
    st.write(f"- % localizadas em área urbana: **{round((df_municipais['localizacao'].str.lower() == 'urbana').mean() * 100, 1)}%**")
    st.write(f"- Portes mais comuns: **{', '.join(df_municipais['porte'].value_counts().head(3).index)}**")

# Tabela de escolas
st.markdown("### 📋 Lista de Escolas")
st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True)
