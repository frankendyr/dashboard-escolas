import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
@st.cache_data
def carregar_dados():
    return pd.read_csv("dashboard_escolas_guaraciaba.csv")

df = carregar_dados()

# Estilo global
st.set_page_config(page_title="Dashboard Educação", layout="wide")

# Título
st.title("📊 Painel de Gestão Educacional")
st.markdown("Indicadores das escolas de Guaraciaba do Norte (CE) — Base: Censo Escolar 2024")
st.markdown("---")

# 📌 Filtros interativos
st.sidebar.header("🔎 Filtros")

zona_opcao = st.sidebar.multiselect("Zona", options=sorted(df['Zona'].dropna().unique()), default=sorted(df['Zona'].dropna().unique()))
categoria_opcao = st.sidebar.multiselect("Categoria", options=sorted(df['Categoria'].dropna().unique()), default=sorted(df['Categoria'].dropna().unique()))
porte_opcao = st.sidebar.multiselect("Porte", options=sorted(df['Porte'].dropna().unique()), default=sorted(df['Porte'].dropna().unique()))

# Aplicar filtros
df_filtrado = df[
    (df['Zona'].isin(zona_opcao)) &
    (df['Categoria'].isin(categoria_opcao)) &
    (df['Porte'].isin(porte_opcao))
]

# Cartões principais
st.markdown("### 📌 Visão Geral")
col1, col2, col3 = st.columns(3)
col1.metric("Total de Escolas", len(df_filtrado))
col2.metric("% Escolas Privadas", f"{(df_filtrado['Categoria'] == 'Privada').mean()*100:.1f}%")
col3.metric("% Escolas em Zona Urbana", f"{(df_filtrado['Zona'] == 'Urbana').mean()*100:.1f}%")

st.markdown("---")

# Gráfico: Categoria administrativa
st.markdown("### 🏫 Categoria Administrativa")
fig_cat = px.pie(df_filtrado, names='Categoria', title='Distribuição: Pública vs Privada')
fig_cat.update_traces(textinfo='percent+label')
st.plotly_chart(fig_cat, use_container_width=True)

# Gráfico: Porte das escolas
st.markdown("### 🧱 Porte das Escolas por Categoria")
fig_porte = px.histogram(df_filtrado, x='Porte', color='Categoria', barmode='group', title="Porte por Categoria")
fig_porte.update_traces(texttemplate='%{y}', textposition='outside')
st.plotly_chart(fig_porte, use_container_width=True)

# Gráfico: Porte por Zona
st.markdown("### 🌍 Porte das Escolas por Zona")
porte_zona = df_filtrado.groupby(['Zona', 'Porte']).size().reset_index(name='Total')
fig_pz = px.bar(porte_zona, x='Zona', y='Total', color='Porte', barmode='group', title='Distribuição por Zona')
fig_pz.update_traces(texttemplate='%{y}', textposition='outside')
st.plotly_chart(fig_pz, use_container_width=True)

# Gráfico: Zona x Categoria
st.markdown("### 🧭 Zona x Categoria Administrativa")
zona_categoria = df_filtrado.groupby(['Zona', 'Categoria']).size().reset_index(name='Total')
fig_zc = px.bar(zona_categoria, x='Zona', y='Total', color='Categoria', barmode='group')
fig_zc.update_traces(texttemplate='%{y}', textposition='outside')
st.plotly_chart(fig_zc, use_container_width=True)

# Gráfico: Etapas de Ensino
st.markdown("### 📚 Etapas de Ensino Oferecidas")
etapas_contagem = df_filtrado['Etapas'].fillna('Não Informado').str.split(', ').explode().value_counts()
fig_etapas = px.bar(x=etapas_contagem.index, y=etapas_contagem.values,
                    labels={'x': 'Etapa', 'y': 'Qtd Escolas'},
                    title='Etapas de Ensino')
fig_etapas.update_traces(texttemplate='%{y}', textposition='outside')
st.plotly_chart(fig_etapas, use_container_width=True)

# Gráfico: Etapas por Categoria
st.markdown("### 🧩 Etapas por Categoria")
etapas_categoria = df_filtrado[['Etapas', 'Categoria']].dropna()
etapas_categoria = etapas_categoria.assign(Etapa=etapas_categoria['Etapas'].str.split(', '))
etapas_categoria = etapas_categoria.explode('Etapa')
grupo = etapas_categoria.groupby(['Categoria', 'Etapa']).size().reset_index(name='Total')
fig_ec = px.bar(grupo, x='Etapa', y='Total', color='Categoria', barmode='group', title='Distribuição de Etapas por Categoria')
fig_ec.update_traces(texttemplate='%{y}', textposition='outside')
st.plotly_chart(fig_ec, use_container_width=True)

# Lista de escolas
st.markdown("### 🗂️ Lista de Escolas")

filtro_categoria = st.selectbox("Filtrar por categoria:", options=['Todas'] + sorted(df_filtrado['Categoria'].dropna().unique()))

if filtro_categoria != 'Todas':
    df_lista = df_filtrado[df_filtrado['Categoria'] == filtro_categoria]
else:
    df_lista = df_filtrado

st.dataframe(df_lista.reset_index(drop=True))
