import streamlit as st
import pandas as pd
import plotly.express as px

# Leitura do CSV com os dados
@st.cache_data
def carregar_dados():
    return pd.read_csv("dashboard_escolas_guaraciaba.csv")

df = carregar_dados()

# Título
st.markdown("""
<h1 style='text-align: center; color: #2C88D9;'>
    🏛️ Painel Educacional — Guaraciaba do Norte (CE)
</h1>
""", unsafe_allow_html=True)

# Filtros
st.sidebar.markdown("## 🔍 Filtros")
categorias = ["Todas"] + sorted(df["categoria_administrativa"].dropna().unique())
zona = ["Todas"] + sorted(df["localizacao"].dropna().unique())
porte = ["Todas"] + sorted(df["porte"].dropna().unique())

categoria = st.sidebar.selectbox("Categoria", categorias)
zona_sel = st.sidebar.selectbox("Zona", zona)
porte_sel = st.sidebar.selectbox("Porte", porte)

# Aplicar filtros
df_filtrado = df.copy()
if categoria != "Todas":
    df_filtrado = df_filtrado[df_filtrado["categoria_administrativa"] == categoria]
if zona_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["localizacao"] == zona_sel]
if porte_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["porte"] == porte_sel]

# KPIs principais
total_escolas = len(df_filtrado)
pct_publicas = (df_filtrado["dependencia_administrativa"].str.lower() == "pública").mean() * 100
pct_urbanas = (df_filtrado["localizacao"].str.lower() == "urbana").mean() * 100

col1, col2, col3 = st.columns(3)
col1.metric("Total de Escolas", total_escolas)
col2.metric("% Públicas", f"{pct_publicas:.1f}%")
col3.metric("% Urbanas", f"{pct_urbanas:.1f}%")

# Comparativo: Escolas Municipais
df_municipais = df_filtrado[df_filtrado['dependencia_administrativa'].str.lower() == 'municipal']
pct_municipais = len(df_municipais) / len(df_filtrado) * 100 if len(df_filtrado) > 0 else 0

st.markdown(f"""
### 🏢 Escolas Municipais
- Total: **{len(df_municipais)}**
- Representam: **{pct_municipais:.1f}%** do total de escolas filtradas
""")

# Gráfico: Distribuição por categoria administrativa
fig_categoria = px.histogram(df_filtrado, x="categoria_administrativa", color="dependencia_administrativa",
                             title="Distribuição por Categoria Administrativa",
                             labels={"categoria_administrativa": "Categoria"})
st.plotly_chart(fig_categoria, use_container_width=True)

# Gráfico: Localização Geográfica das Escolas
st.map(df_filtrado[['latitude', 'longitude']].dropna(), zoom=12)
