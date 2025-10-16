# ======================================================
# DASHBOARD STREAMLIT - ODS 4: EDUCAÇÃO DE QUALIDADE
# Versão adaptada para execução no Google Colab
# ======================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ======================================================
# CONFIGURAÇÃO DA PÁGINA
# ======================================================
st.set_page_config(
    page_title="ODS 4: Educação de Qualidade - Impactos da COVID-19",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📚 ODS 4: Educação de Qualidade")
st.subheader("Impactos da COVID-19 na Aprendizagem dos Estudantes")

# ======================================================
# FUNÇÃO PARA CARREGAR OS DADOS
# ======================================================
@st.cache_data
def load_data():
    # Caminho automático para CSV no Colab
    csv_path = "Chart6_student_learning_impacts.csv"
    if not os.path.exists(csv_path):
        st.error("❌ O arquivo 'Chart6_student_learning_impacts.csv' não foi encontrado. "
                 "Envie o arquivo para o Colab antes de executar o app.")
        st.stop()
    return pd.read_csv(csv_path)

df = load_data()

# ======================================================
# SIDEBAR DE NAVEGAÇÃO
# ======================================================
st.sidebar.title("Navegação")
page = st.sidebar.selectbox(
    "Escolha uma seção:",
    ["Visão Geral", "Análise Exploratória", "Visualizações Interativas", "Insights e Conclusões"]
)

# ======================================================
# VISÃO GERAL
# ======================================================
if page == "Visão Geral":
    st.markdown("---")
    st.markdown("""
    ## Sobre o ODS 4: Educação de Qualidade
    
    O **Objetivo de Desenvolvimento Sustentável 4** visa garantir educação inclusiva, equitativa e de qualidade,
    promovendo oportunidades de aprendizagem ao longo da vida para todos até 2030.
    
    ### Dataset: Impactos da COVID-19 na Aprendizagem
    
    Este dashboard apresenta dados sobre os impactos da pandemia de COVID-19 na aprendizagem dos estudantes 
    em diferentes países, analisando a relação entre o tempo de fechamento das escolas e as perdas de aprendizagem.
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Países Analisados", len(df))
    with col2:
        st.metric("Média de Semanas de Fechamento", f"{df['Closure length weeks'].mean():.1f}")
    with col3:
        st.metric("Maior Perda de Aprendizagem", f"{df['Average learning losses (SD)'].min():.2f} SD", delta="México")
    with col4:
        st.metric("Média de Anos Perdidos", f"{abs(df['years_lost'].mean()):.2f}")
    
    st.markdown("### Dados Completos")
    st.dataframe(df, use_container_width=True)

# ======================================================
# ANÁLISE EXPLORATÓRIA
# ======================================================
elif page == "Análise Exploratória":
    st.markdown("---")
    st.markdown("## Análise Exploratória de Dados")

    st.markdown("### Estatísticas Descritivas")
    st.dataframe(df.describe(), use_container_width=True)

    st.markdown("### Distribuição das Variáveis")
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.histogram(df, x="Closure length weeks", nbins=10,
                            title="Distribuição das Semanas de Fechamento",
                            color_discrete_sequence=["#1f77b4"])
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = px.histogram(df, x="Average learning losses (SD)", nbins=10,
                            title="Distribuição das Perdas de Aprendizagem",
                            color_discrete_sequence=["#ff7f0e"])
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### Matriz de Correlação")
    numeric_cols = ["Closure length weeks", "Average learning losses (SD)", "share_closed", "years_lost"]
    corr = df[numeric_cols].corr()
    fig_corr = px.imshow(corr, text_auto=True, aspect="auto",
                         title="Matriz de Correlação entre Variáveis Numéricas",
                         color_continuous_scale="RdBu_r")
    st.plotly_chart(fig_corr, use_container_width=True)

# ======================================================
# VISUALIZAÇÕES INTERATIVAS
# ======================================================
elif page == "Visualizações Interativas":
    st.markdown("---")
    st.markdown("## Visualizações Interativas")

    st.markdown("### Relação entre Fechamento de Escolas e Perdas de Aprendizagem")
    fig_scatter = px.scatter(
        df, x="Closure length weeks", y="Average learning losses (SD)",
        hover_data=["Country"], color="years_lost", size="share_closed",
        color_continuous_scale="Viridis",
        title="Semanas de Fechamento vs. Perdas de Aprendizagem"
    )
    fig_scatter.add_traces(px.scatter(df, x="Closure length weeks", y="Average learning losses (SD)",
                                      trendline="ols").data[1])
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("### Perdas de Aprendizagem por País (Ordenado)")
    df_sorted = df.sort_values("Average learning losses (SD)")
    fig_bar = px.bar(df_sorted, x="Country", y="Average learning losses (SD)",
                     color="Average learning losses (SD)", color_continuous_scale="Reds",
                     title="Perdas de Aprendizagem por País")
    fig_bar.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("### Filtros Interativos")
    weeks_range = st.slider("Filtrar por Semanas de Fechamento:",
                            int(df["Closure length weeks"].min()),
                            int(df["Closure length weeks"].max()),
                            (int(df["Closure length weeks"].min()), int(df["Closure length weeks"].max())))
    filtered = df[(df["Closure length weeks"] >= weeks_range[0]) &
                  (df["Closure length weeks"] <= weeks_range[1])]
    st.markdown(f"**Países selecionados:** {len(filtered)}")
    st.dataframe(filtered[["Country", "Closure length weeks", "Average learning losses (SD)"]], use_container_width=True)

# ======================================================
# INSIGHTS E CONCLUSÕES
# ======================================================
elif page == "Insights e Conclusões":
    st.markdown("---")
    st.markdown("## Insights e Conclusões")

    st.markdown("""
    ### 🔍 Principais Insights
    1. **Correlação Forte:** Correlação negativa entre tempo de fechamento e perdas de aprendizagem (-0.76).
    2. **México como Outlier:** Maior perda de aprendizagem (-0.55 SD) e 48 semanas de fechamento.
    3. **Variação Significativa:** Fechamentos variaram de 7 a 48 semanas entre os países.
    4. **Impacto Quantificável:** Média de 0.54 anos de aprendizagem perdidos.
    """)

    st.markdown("""
    ### 📋 Recomendações
    - Minimizar fechamentos de escolas.
    - Investir em infraestrutura de ensino remoto.
    - Implementar programas de recuperação de aprendizagem.
    - Monitorar continuamente os indicadores educacionais.
    """)

    st.markdown("""
    ### ⚠️ Limitações
    - Amostra pequena (19 países).
    - Metodologias diferentes entre estudos.
    - Fatores socioeconômicos não considerados.
    """)

    st.markdown("""
    ### 🚀 Próximos Passos
    1. Expandir dataset para mais países.
    2. Adicionar dados temporais (anos).
    3. Analisar por faixa etária e gênero.
    4. Criar modelo preditivo de impacto futuro.
    """)

# ======================================================
# RODAPÉ
# ======================================================
st.markdown("---")
st.markdown("""
**Fonte dos Dados:** World Bank SDG Atlas 2023 - Goal 4: Quality Education  
**Desenvolvido por:** Caio Barbosa, Davi Vaz e Lucas Almeida  
**Última Atualização:** Outubro 2025
""")
