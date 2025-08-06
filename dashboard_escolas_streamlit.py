import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
@st.cache_data
def carregar_dados():
    return pd.read_csv("dashboard_escolas_guaraciaba.csv")

df = carregar_dados()

# Título
st.title("📈 Painel de Gestão - Escolas de Guaraciaba do Norte (CE)")
st.markdown("Dashboard objetivo com indicadores educacionais municipais. Base: Censo Escolar")

# Cartões principais
col1, col2, col3 = st.columns(3)
col1.metric("Total de Escolas", len(df))
col2.metric("% Escolas Privadas", f"{(df['Categoria'] == 'Privada').mean()*100:.1f}%")
col3.metric("% Escolas em Zona Urbana", f"{(df['Zona'] == 'Urbana').mean()*100:.1f}%")

# Gráfico: Categoria administrativa
st.subheader("Distribuição por Categoria Administrativa")
fig_cat = px.pie(df, names='Categoria', title='Pública vs Privada')
st.plotly_chart(fig_cat)

# Gráfico: Porte das escolas
st.subheader("Distribuição por Porte das Escolas")
fig_porte = px.histogram(df, x='Porte', color='Categoria', barmode='group')
st.plotly_chart(fig_porte)

# Gráfico: Etapas de ensino (resumo)
st.subheader("Etapas de Ensino Oferecidas")
etapas_contagem = df['Etapas'].fillna('Não Informado').str.split(', ').explode().value_counts()
fig_etapas = px.bar(x=etapas_contagem.index, y=etapas_contagem.values, labels={'x': 'Etapa', 'y': 'Qtd Escolas'})
st.plotly_chart(fig_etapas)

# Nova Visão: Zona x Categoria
st.subheader("Zona x Categoria Administrativa")
zona_categoria = df.groupby(['Zona', 'Categoria']).size().reset_index(name='Total')
fig_zc = px.bar(zona_categoria, x='Zona', y='Total', color='Categoria', barmode='group')
st.plotly_chart(fig_zc)

# Nova Visão: Etapas x Categoria
st.subheader("Etapas de Ensino por Categoria")
etapas_categoria = df[['Etapas', 'Categoria']].dropna()
etapas_categoria = etapas_categoria.assign(Etapa=etapas_categoria['Etapas'].str.split(', '))
etapas_categoria = etapas_categoria.explode('Etapa')
grupo = etapas_categoria.groupby(['Categoria', 'Etapa']).size().reset_index(name='Total')
fig_ec = px.bar(grupo, x='Etapa', y='Total', color='Categoria', barmode='group')
st.plotly_chart(fig_ec)

# Nova Visão: Porte x Zona
st.subheader("Distribuição do Porte das Escolas por Zona")
porte_zona = df.groupby(['Zona', 'Porte']).size().reset_index(name='Total')
fig_pz = px.bar(porte_zona, x='Zona', y='Total', color='Porte', barmode='group')
st.plotly_chart(fig_pz)

# Nova Visão: Total por Porte
st.subheader("Total de Escolas por Porte")
fig_total_porte = px.pie(df, names='Porte', title='Distribuição do Porte das Escolas')
st.plotly_chart(fig_total_porte)

# Tabela detalhada com filtro
st.subheader("📄 Lista de Escolas")
filtro_categoria = st.selectbox("Filtrar por categoria:", options=['Todas'] + sorted(df['Categoria'].dropna().unique()))

if filtro_categoria != 'Todas':
    df_filtrado = df[df['Categoria'] == filtro_categoria]
else:
    df_filtrado = df

st.dataframe(df_filtrado.reset_index(drop=True))
