import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(
    page_title="Painel Educacional — Guaraciaba do Norte (CE)",
    layout="wide",
    page_icon="🏛️"
)

st.markdown("<h1 style='text-align: center;'>🏛️ Painel Educacional — Guaraciaba do Norte (CE)</h1>", unsafe_allow_html=True)

# Carregamento dos dados
@st.cache_data
def carregar_dados():
    df = pd.read_csv("dashboard_escolas_guaraciaba.csv")
    return df

df = carregar_dados()

# Filtros
st.sidebar.title("🔍 Filtros")
categorias = ["Todas"] + sorted(df["categoria_administrativa"].dropna().unique())
zona = ["Todas"] + sorted(df["localizacao"].dropna().unique())
porte = ["Todas"] + sorted(df["porte"].dropna().unique())

categoria_sel = st.sidebar.selectbox("Categoria", categorias)
zona_sel = st.sidebar.selectbox("Zona", zona)
porte_sel = st.sidebar.selectbox("Porte", porte)

df_filtrado = df.copy()

if categoria_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["categoria_administrativa"] == categoria_sel]

if zona_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["localizacao"] == zona_sel]

if porte_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["porte"] == porte_sel]

# Métricas principais
total_escolas = len(df_filtrado)
total_municipais = len(df_filtrado[df_filtrado["categoria_administrativa"].str.lower() == "pública"])
perc_municipais = round((total_municipais / total_escolas) * 100, 1) if total_escolas > 0 else 0
perc_urbanas = round((len(df_filtrado[df_filtrado["localizacao"].str.lower() == "urbana"]) / total_escolas) * 100, 1) if total_escolas > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total de Escolas", total_escolas)
col2.metric("% Municipais", f"{perc_municipais}%")
col3.metric("% Urbanas", f"{perc_urbanas}%")

st.markdown("### 📊 Gráficos Educacionais")

# Gráfico 1: Categoria Administrativa
st.subheader("Distribuição por Categoria Administrativa")
fig1, ax1 = plt.subplots()
df_filtrado["categoria_administrativa"].value_counts().plot(kind="bar", color="#4C72B0", ax=ax1)
ax1.set_xlabel("Categoria")
ax1.set_ylabel("Nº de Escolas")
st.pyplot(fig1)

# Gráfico 2: Localização
st.subheader("Distribuição por Localização")
fig2, ax2 = plt.subplots()
df_filtrado["localizacao"].value_counts().plot(kind="bar", color="#55A868", ax=ax2)
ax2.set_xlabel("Localização")
ax2.set_ylabel("Nº de Escolas")
st.pyplot(fig2)

# Gráfico 3: Porte das Escolas
st.subheader("Distribuição por Porte")
fig3, ax3 = plt.subplots()
df_filtrado["porte"].value_counts().plot(kind="bar", color="#C44E52", ax=ax3)
ax3.set_xlabel("Porte")
ax3.set_ylabel("Nº de Escolas")
st.pyplot(fig3)

# Tabela detalhada
st.markdown("### 🏫 Lista de Escolas")
st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True)
