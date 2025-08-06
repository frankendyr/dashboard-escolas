import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
@st.cache_data

def carregar_dados():
    df = pd.read_csv("dashboard_escolas_guaraciaba.csv")
    df["etapas_modalidades_oferecidas"] = df["etapas_modalidades_oferecidas"].fillna("Nao Informado")
    return df

df = carregar_dados()

# Sidebar - Filtros
st.sidebar.title("🔍 Filtros")

zona_opcoes = df["localizacao"].dropna().unique().tolist()
categoria_opcoes = df["categoria_administrativa"].dropna().unique().tolist()
porte_opcoes = df["porte"].dropna().unique().tolist()

zona = st.sidebar.multiselect("Zona", options=zona_opcoes, default=zona_opcoes)
categoria = st.sidebar.multiselect("Categoria", options=categoria_opcoes, default=categoria_opcoes)
porte = st.sidebar.multiselect("Porte", options=porte_opcoes, default=porte_opcoes)

# Aplicar filtros
df_filtrado = df[
    df["localizacao"].isin(zona) &
    df["categoria_administrativa"].isin(categoria) &
    df["porte"].isin(porte)
]

# Título
titulo = "📊 Painel de Gestão Educacional"
st.markdown(f"<h1 style='color:white'>{titulo}</h1>", unsafe_allow_html=True)
st.markdown("Indicadores das escolas de Guaraciaba do Norte (CE) — Base: Censo Escolar 2024")
st.markdown("---")

# Métricas principais
col1, col2, col3 = st.columns(3)
col1.metric("Total de Escolas", len(df_filtrado))
col2.metric("% Escolas Privadas", f"{(df_filtrado['categoria_administrativa'] == 'Privada').mean()*100:.1f}%")
col3.metric("% Escolas em Zona Urbana", f"{(df_filtrado['localizacao'] == 'Urbana').mean()*100:.1f}%")

# Gráficos principais
st.subheader("🏫 Categoria Administrativa")
fig_cat = px.pie(df_filtrado, names='categoria_administrativa', title='Pública vs Privada', hole=0.4)
st.plotly_chart(fig_cat, use_container_width=True)

st.subheader("📊 Porte das Escolas")
fig_porte = px.histogram(df_filtrado, x='porte', color='categoria_administrativa', barmode='group')
st.plotly_chart(fig_porte, use_container_width=True)

st.subheader("📚 Etapas de Ensino Oferecidas")
etapas = df_filtrado['etapas_modalidades_oferecidas'].str.split(', ').explode().value_counts()
fig_etapas = px.bar(x=etapas.index, y=etapas.values, labels={'x': 'Etapa', 'y': 'Qtd Escolas'})
st.plotly_chart(fig_etapas, use_container_width=True)

st.subheader("📍 Zona x Categoria Administrativa")
zona_categoria = df_filtrado.groupby(['localizacao', 'categoria_administrativa']).size().reset_index(name='Total')
fig_zc = px.bar(zona_categoria, x='localizacao', y='Total', color='categoria_administrativa', barmode='group')
st.plotly_chart(fig_zc, use_container_width=True)

st.subheader("🏷️ Etapas x Categoria")
etapas_categoria = df_filtrado[['etapas_modalidades_oferecidas', 'categoria_administrativa']].dropna()
etapas_categoria = etapas_categoria.assign(Etapa=etapas_categoria['etapas_modalidades_oferecidas'].str.split(', '))
etapas_categoria = etapas_categoria.explode('Etapa')
grupo = etapas_categoria.groupby(['categoria_administrativa', 'Etapa']).size().reset_index(name='Total')
fig_ec = px.bar(grupo, x='Etapa', y='Total', color='categoria_administrativa', barmode='group')
st.plotly_chart(fig_ec, use_container_width=True)

st.subheader("🏘️ Porte x Zona")
porte_zona = df_filtrado.groupby(['localizacao', 'porte']).size().reset_index(name='Total')
fig_pz = px.bar(porte_zona, x='localizacao', y='Total', color='porte', barmode='group')
st.plotly_chart(fig_pz, use_container_width=True)

st.subheader("📊 Total por Porte")
fig_total_porte = px.pie(df_filtrado, names='porte', title='Distribuição por Porte', hole=0.3)
st.plotly_chart(fig_total_porte, use_container_width=True)

# Tabela detalhada
st.subheader("📄 Lista de Escolas")
st.dataframe(df_filtrado.reset_index(drop=True))
