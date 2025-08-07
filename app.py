import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =====================
# Leitura dos dados
# =====================
df = pd.read_csv("dashboard_escolas_guaraciaba.csv")

# =====================
# Título do painel
# =====================
st.markdown("<h1 style='text-align: center;'>🏛️ Painel Educacional — Guaraciaba do Norte (CE)</h1>", unsafe_allow_html=True)

# =====================
# Filtros
# =====================
st.sidebar.header("🔎 Filtros")

categorias = ["Todas"] + sorted(df["categoria_administrativa"].dropna().unique())
categoria = st.sidebar.selectbox("Categoria", categorias)

zonas = ["Todas"] + sorted(df["localizacao"].dropna().unique())
zona = st.sidebar.selectbox("Zona", zonas)

portes = ["Todas"] + sorted(df["porte"].dropna().unique())
porte = st.sidebar.selectbox("Porte", portes)

# Aplicando filtros
df_filtrado = df.copy()
if categoria != "Todas":
    df_filtrado = df_filtrado[df_filtrado["categoria_administrativa"] == categoria]
if zona != "Todas":
    df_filtrado = df_filtrado[df_filtrado["localizacao"] == zona]
if porte != "Todas":
    df_filtrado = df_filtrado[df_filtrado["porte"] == porte]

# =====================
# Métricas principais
# =====================
total_escolas = len(df_filtrado)
escolas_municipais = df_filtrado[df_filtrado["categoria_administrativa"].str.lower() == "municipal"]
percentual_municipais = (len(escolas_municipais) / total_escolas * 100) if total_escolas > 0 else 0
percentual_urbanas = (len(df_filtrado[df_filtrado["localizacao"].str.lower() == "urbana"]) / total_escolas * 100) if total_escolas > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total de Escolas", total_escolas)
col2.metric("% Municipais", f"{percentual_municipais:.1f}%")
col3.metric("% Urbanas", f"{percentual_urbanas:.1f}%")

# =====================
# Detalhes Municipais
# =====================
st.markdown("### 🏫 Detalhes das Escolas Municipais")

st.markdown(f"- Total de escolas municipais: **{len(escolas_municipais)}**")
st.markdown(f"- % do total: **{percentual_municipais:.1f}%**")
percent_urb_mun = (len(escolas_municipais[escolas_municipais['localizacao'].str.lower() == "urbana"]) / len(escolas_municipais) * 100) if len(escolas_municipais) > 0 else 0
st.markdown(f"- % localizadas em área urbana: **{percent_urb_mun:.1f}%**")
portes_comuns = escolas_municipais["porte"].value_counts().head(3).index.tolist()
st.markdown(f"- Portes mais comuns: **{', '.join(portes_comuns)}**")

# =====================
# Gráficos
# =====================
st.markdown("### 📊 Gráficos")

col_g1, col_g2 = st.columns(2)

with col_g1:
    st.image("graficos_escolas/grafico_categoria_administrativa.png", caption="Categoria Administrativa")
    st.image("graficos_escolas/grafico_dependencia_administrativa.png", caption="Dependência Administrativa")

with col_g2:
    st.image("graficos_escolas/grafico_localizacao.png", caption="Localização")
    st.image("graficos_escolas/grafico_porte.png", caption="Porte")

# =====================
# Tabela de Escolas
# =====================
st.markdown("### 📋 Lista de Escolas")
st.dataframe(df_filtrado.reset_index(drop=True))
