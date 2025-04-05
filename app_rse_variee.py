
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# --- Logo ---
logo = Image.open("logo_rse_streamlit.png")
st.image(logo, width=120)

# --- Titre stylisé ---
st.markdown("<h1 style='text-align: center; color: #6a0dad;'>🌿 Dashboard RSE interactif</h1>", unsafe_allow_html=True)

# --- Sidebar : lien de partage ---
with st.sidebar:
    st.markdown("📤 **Partager cette app**")
    st.code("https://app-rse-eg4fwvdtkmi9jqfaxe9fls.streamlit.app/")
    st.markdown(
        f"[🔗 Ouvrir dans un nouvel onglet](https://app-rse-eg4fwvdtkmi9jqfaxe9fls.streamlit.app/)",
        unsafe_allow_html=True
    )

# --- Chargement des données CSV ---
uploaded_file = st.file_uploader("📁 Importez votre fichier CSV au bon format", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # --- Filtres interactifs ---
    st.sidebar.header("🔎 Filtres interactifs")
    themes = st.sidebar.multiselect("🎯 Thème RSE", options=df["Thème RSE"].unique(), default=df["Thème RSE"].unique())
    entreprises = st.sidebar.multiselect("🏢 Entreprises", options=df["Entreprise"].unique(), default=df["Entreprise"].unique())
    score_min = st.sidebar.slider("🌡️ Score RSE minimal", min_value=0, max_value=100, value=50)

    df_filtre = df[(df["Thème RSE"].isin(themes)) & (df["Entreprise"].isin(entreprises)) & (df["Score"] >= score_min)]

    st.subheader("📑 Aperçu des données filtrées")
    st.dataframe(df_filtre.head())

    score_moy = df_filtre.groupby("Entreprise")["Score"].mean().reset_index().sort_values(by="Score", ascending=False)
    st.subheader("📈 Scores RSE moyens par entreprise")
    fig = px.bar(score_moy, x="Entreprise", y="Score", color="Score", color_continuous_scale="viridis")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🎯 Jauge du Score Moyen Global")
    moyenne_globale = score_moy["Score"].mean()
    fig_jauge = px.pie(values=[moyenne_globale, 100 - moyenne_globale], names=["Score Moyen", "Reste"], hole=0.7,
                       color_discrete_sequence=["#6a0dad", "#e8e8e8"])
    fig_jauge.update_traces(textinfo='percent+label')
    st.plotly_chart(fig_jauge, use_container_width=True)

    csv_export = score_moy.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Exporter les résultats", csv_export, "scores_rse_filtrés.csv", "text/csv")

st.markdown("<hr><p style='text-align: center;'>🚀 Mémoire Data Analytics | Hibat Allah Bachterzi | 2025</p>", unsafe_allow_html=True)
