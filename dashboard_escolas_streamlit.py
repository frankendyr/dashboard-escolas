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

# Mapa
st.subheader("🗺️ Mapa de Localização das Escolas")
map_df = df.dropna(subset=['Latitude', 'Longitude'])
# Corrigir tipos e remover dados inválidos
map_df = map_df.copy()
map_df['Latitude'] = pd.to_numeric(map_df['Latitude'], errors='coerce')
map_df['Longitude'] = pd.to_numeric(map_df['Longitude'], errors='coerce')
map_df = map_df.dropna(subset=['Latitude', 'Longitude'])

st.map(map_df[['Latitude', 'Longitude']])

# Tabela detalhada com filtro
st.subheader("📄 Lista de Escolas")
filtro_categoria = st.selectbox("Filtrar por categoria:", options=['Todas'] + sorted(df['Categoria'].dropna().unique()))

if filtro_categoria != 'Todas':
    df_filtrado = df[df['Categoria'] == filtro_categoria]
else:
    df_filtrado = df

st.dataframe(df_filtrado.reset_index(drop=True))
