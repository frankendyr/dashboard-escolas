import streamlit as st
import pandas as pd
import plotly.express as px

# ========= CONFIGURAÇÃO DO APP =========
st.set_page_config(
    page_title="Painel de Gestão Educacional",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========= ESTILO CUSTOMIZADO =========
st.markdown("""
    <style>
    .main {
        background-color: #F5F8FA;
    }
    .stMetric {
        background-color: #E3F2FD;
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
    }
    .block-container {
        padding: 2rem 2rem 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# ========= CARREGAMENTO DOS DADOS =========
@st.cache_data
def carregar_dados():
    return pd.read_csv("dashboard_escolas_guaraciaba.csv")

df = carregar_dados()

# ========= BARRA LATERAL - FILTROS =========
st.sidebar.header("🔍 Filtros")
zonas = st.sidebar.multiselect("Zona", df["Zona"].dropna().unique(), default=list(df["Zona"].dropna().unique()))
categorias = st.sidebar.multiselect("Categoria", df["Categoria"].dropna().unique(), default=list(df["Categoria"].dropna().unique()))
portes = st.sidebar.multiselect("Porte", df["Porte"].dropna().unique(), default=list(df["Porte"].dropna().unique()))

# ========= APLICAÇÃO DOS FILTROS =========
df_filtrado = df[
    (df["Zona"].isin(zonas)) &
    (df["Categoria"].isin(categorias)) &
    (df["Porte"].isin(portes))
]

# ========= TÍTULO =========
st.title("📊 Painel de Gestão Educacional")
st.markdown("Indicadores das escolas de Guaraciaba do Norte (CE) — Base: Censo Escolar 2024")
st.markdown("---")

# ========= MÉTRICAS PRINCIPAIS =========
col1, col2, col3 = st.columns(3)
col1.metric("Total de Escolas", len(df_filtrado))
col2.metric("% Escolas Privadas", f"{(df_filtrado['Categoria'] == 'Privada').mean()*100:.1f}%")
col3.metric("% Escolas em Zona Urbana", f"{(df_filtrado['Zona'] == 'Urbana').mean()*100:.1f}%")
st.markdown("---")

# ========= GRÁFICO: Categoria Administrativa =========
st.subheader("🏫 Categoria Administrativa")
fig_cat = px.pie(df_filtrado, names='Categoria', title='Pública vs Privada', hole=0.3)
st.plotly_chart(fig_cat, use_container_width=True)

# ========= GRÁFICO: Porte das Escolas =========
st.subheader("📦 Porte das Escolas")
fig_porte = px.histogram(df_filtrado, x='Porte', color='Categoria', barmode='group')
st.plotly_chart(fig_porte, use_container_width=True)

# ========= GRÁFICO: Etapas de Ensino =========
st.subheader("📚 Etapas de Ensino Oferecidas")
etapas_contagem = df_filtrado['Etapas'].fillna('Não Informado').str.split(', ').explode().value_counts()
fig_etapas = px.bar(x=etapas_contagem.index, y=etapas_contagem.values,
                    labels={'x': 'Etapa', 'y': 'Qtd Escolas'})
st.plotly_chart(fig_etapas, use_container_width=True)

# ========= GRÁFICO: Zona x Categoria =========
st.subheader("🌐 Zona x Categoria Administrativa")
zona_categoria = df_filtrado.groupby(['Zona', 'Categoria']).size().reset_index(name='Total')
fig_zc = px.bar(zona_categoria, x='Zona', y='Total', color='Categoria', barmode='group')
st.plotly_chart(fig_zc, use_container_width=True)

# ========= GRÁFICO: Etapas x Categoria =========
st.subheader("🧩 Etapas por Categoria")
etapas_categoria = df_filtrado[['Etapas', 'Categoria']].dropna()
etapas_categoria = etapas_categoria.assign(Etapa=etapas_categoria['Etapas'].str.split(', '))
etapas_categoria = etapas_categoria.explode('Etapa')
grupo = etapas_categoria.groupby(['Categoria', 'Etapa']).size().reset_index(name='Total')
fig_ec = px.bar(grupo, x='Etapa', y='Total', color='Categoria', barmode='group')
st.plotly_chart(fig_ec, use_container_width=True)

# ========= GRÁFICO: Porte x Zona =========
st.subheader("📍 Porte x Zona")
porte_zona = df_filtrado.groupby(['Zona', 'Porte']).size().reset_index(name='Total')
fig_pz = px.bar(porte_zona, x='Zona', y='Total', color='Porte', barmode='group')
st.plotly_chart(fig_pz, use_container_width=True)

# ========= GRÁFICO: Total por Porte =========
st.subheader("📊 Total de Escolas por Porte")
fig_total_porte = px.pie(df_filtrado, names='Porte', title='Distribuição do Porte', hole=0.3)
st.plotly_chart(fig_total_porte, use_container_width=True)

# ========= TABELA DETALHADA =========
st.subheader("📋 Lista de Escolas")
st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True)
