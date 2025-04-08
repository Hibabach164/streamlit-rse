
import streamlit as st
import pandas as pd
import plotly.express as px

# Chargement des données
df = pd.read_csv("donnees_rse_1.csv")

st.set_page_config(page_title="Dashboard RSE", layout="wide")

st.title("🌱 Dashboard RSE - Analyse des Scores par Entreprise et Thème")

# Filtres
entreprises = st.sidebar.multiselect("Sélectionnez une ou plusieurs entreprises :", options=df["Entreprise"].unique(), default=df["Entreprise"].unique())
themes = st.sidebar.multiselect("Sélectionnez un ou plusieurs thèmes RSE :", options=df["Thème RSE"].unique(), default=df["Thème RSE"].unique())

# Filtrage des données
filtered_df = df[(df["Entreprise"].isin(entreprises)) & (df["Thème RSE"].isin(themes))]

# Score moyen global
mean_score_global = round(filtered_df["Score RSE"].mean(), 2)
st.metric("Score RSE moyen (filtré)", f"{mean_score_global}")

# Moyenne par thème
mean_by_theme = filtered_df.groupby("Thème RSE")["Score RSE"].mean().reset_index()

# Graphique : Score moyen par thème
fig_theme = px.bar(mean_by_theme, x="Thème RSE", y="Score RSE", color="Thème RSE",
                   title="Score RSE moyen par Thème", text_auto=True)
st.plotly_chart(fig_theme, use_container_width=True)

# Graphique : Score par indicateur
fig_indicateur = px.bar(filtered_df, x="Indicateur", y="Score", color="Thème RSE",
                        title="Score par indicateur", barmode="group", text_auto=True)
st.plotly_chart(fig_indicateur, use_container_width=True)

# Affichage du tableau filtré
st.subheader("Données filtrées")
st.dataframe(filtered_df)
