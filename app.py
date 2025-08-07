import streamlit as st
import pandas as pd
import plotly.express as px
import unicodedata

# Padronizar nomes de colunas
def normalize_column(col):
    col = col.lower()
    col = unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('utf-8')
    col = col.strip().replace(' ', '_')
    return col

# Carregar dados
df = pd.read_csv("dashboard_escolas_guaraciaba.csv")
df.columns = [normalize_column(col) for col in df.columns]

# Título
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>🏛️ Painel Educacional — Guaraciaba do Norte (CE)</h1>", unsafe_allow_html=True)

# Filtros
st.sidebar.header("🔎 Filtros")

categorias = ["Todas"] + sorted(df["categoria_administrativa"].dropna().unique())
categoria = st.sidebar.selectbox("Categoria", categorias)

zonas = ["Todas"] + sorted(df["localizacao"].dropna().unique())
zona = st.sidebar.selectbox("Zona", zonas)

portes = ["Todas"] + sorted(df["porte"].dropna().unique())
porte = st.sidebar.selectbox("Porte", portes)

# Aplicar filtros
df_filtrado = df.copy()
if categoria != "Todas":
    df_filtrado = df_filtrado[df_filtrado["categoria_administrativa"] == categoria]
if zona != "Todas":
    df_filtrado = df_filtrado[df_filtrado["localizacao"] == zona]
if porte != "Todas":
    df_filtrado = df_filtrado[df_filtrado["porte"] == porte]

# Indicadores
total_escolas = len(df_filtrado)
perc_publicas = len(df_filtrado[df_filtrado["dependencia_administrativa"].str.lower() == "publica"]) / total_escolas * 100 if total_escolas > 0 else 0
perc_urbanas = len(df_filtrado[df_filtrado["localizacao"].str.lower() == "urbana"]) / total_escolas * 100 if total_escolas > 0 else 0
perc_municipais = len(df_filtrado[df_filtrado["dependencia_administrativa"].str.lower() == "municipal"]) / total_escolas * 100 if total_escolas > 0 else 0

# Cards
card_html = f"""
<div style='display: flex; justify-content: space-around; font-size:20px;'>
    <div><b>Total de Escolas</b><br><span style='font-size: 32px;'>{total_escolas}</span></div>
    <div><b>% Públicas</b><br><span style='font-size: 32px;'>{perc_publicas:.1f}%</span></div>
    <div><b>% Municipais</b><br><span style='font-size: 32px;'>{perc_municipais:.1f}%</span></div>
    <div><b>% Urbanas</b><br><span style='font-size: 32px;'>{perc_urbanas:.1f}%</span></div>
</div>
"""
st.markdown(card_html, unsafe_allow_html=True)
st.markdown("---")

# Gráficos de pizza
if total_escolas > 0:
    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.pie(df_filtrado, names="dependencia_administrativa", title="Distribuição por Dependência Administrativa")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.pie(df_filtrado, names="localizacao", title="Distribuição por Localização")
        st.plotly_chart(fig2, use_container_width=True)

    # Gráfico de barras
    st.markdown("### 📊 Distribuição por Porte e Categoria")
    df_grouped = df_filtrado.groupby(["porte", "categoria_administrativa"]).size().reset_index(name="Quantidade")
    fig3 = px.bar(df_grouped, x="porte", y="Quantidade", color="categoria_administrativa", barmode="group")
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("⚠️ Nenhuma escola encontrada com os filtros selecionados.")
