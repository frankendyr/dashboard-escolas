import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Título
st.title("📊 Painel Educacional - Guaraciaba do Norte (CE)")

# Carregando os dados
@st.cache_data
def carregar_dados():
    return pd.read_csv("dashboard_escolas_guaraciaba.csv")

df = carregar_dados()

# Filtros laterais
st.sidebar.header("🔍 Filtros")

zona = st.sidebar.multiselect("Zona", options=df["Zona"].unique(), default=df["Zona"].unique())
categoria = st.sidebar.multiselect("Categoria", options=df["Categoria"].unique(), default=df["Categoria"].unique())
porte = st.sidebar.multiselect("Porte", options=df["Porte"].unique(), default=df["Porte"].unique())

# Filtrando dados
df_filtrado = df[
    (df["Zona"].isin(zona)) &
    (df["Categoria"].isin(categoria)) &
    (df["Porte"].isin(porte))
]

# Métricas principais
col1, col2, col3 = st.columns(3)

col1.metric("Total de Escolas", len(df_filtrado))
col2.metric("% Escolas Públicas", f"{round((df_filtrado['Categoria'].value_counts(normalize=True).get('Pública', 0)*100), 1)}%")
col3.metric("% Escolas Rurais", f"{round((df_filtrado['Zona'].value_counts(normalize=True).get('Rural', 0)*100), 1)}%")

st.markdown("---")

# Gráficos
col1, col2 = st.columns(2)

with col1:
    fig1 = px.pie(df_filtrado, names='Categoria', title='Distribuição por Categoria')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.pie(df_filtrado, names='Zona', title='Distribuição por Zona')
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    fig3 = px.bar(df_filtrado['Porte'].value_counts().sort_values(), 
                  orientation='h', title='Distribuição por Porte')
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    etapas_series = df_filtrado['Etapas'].str.get_dummies(sep=",").sum().sort_values(ascending=True)
    fig4 = px.bar(etapas_series, orientation='h', title='Quantidade por Etapas de Ensino')
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# Tabela
st.subheader("📄 Tabela de Escolas")
st.dataframe(df_filtrado, use_container_width=True)
