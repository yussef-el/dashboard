import streamlit as st

import pandas as pd

import plotly.express as px

import matplotlib.pyplot as plt

import unicodedata



# Fonction pour nettoyer les noms de colonnes (via unicodedata)

def clean_column_names(df):

    new_columns = []

    for col in df.columns:

        # Enlève les accents et convertit en minuscules

        nfkd_form = unicodedata.normalize('NFKD', str(col))

        clean_name = "".join([c for c in nfkd_form if not unicodedata.combining(c)])

        new_columns.append(clean_name.lower().strip().replace(" ", "_"))

    df.columns = new_columns

    return df



st.set_page_config(page_title="Analyseur Pro CSV/Excel", layout="wide")



st.title("📊 Analyseur de Données Multi-Formats")

st.write("Format supportés : **CSV, XLSX, XLS**")



# Upload du fichier

file = st.file_uploader("Déposez votre fichier ici", type=["csv", "xlsx", "xls"])



if file:

    # Lecture selon l'extension

    if file.name.endswith('.csv'):

        df = pd.read_csv(file)

    else:

        df = pd.read_excel(file)

    

    # Nettoyage automatique

    df = clean_column_names(df)

    

    st.success(f"Fichier '{file.name}' chargé et nettoyé !")

    

    # Affichage des données

    with st.expander("👁️ Voir les données brutes"):

        st.dataframe(df)



    # Configuration des graphiques

    st.divider()

    col1, col2 = st.columns(2)

    

    with col1:

        x_col = st.selectbox("Axe X", options=df.columns)

        y_col = st.selectbox("Axe Y", options=df.columns)

    

    with col2:

        engine = st.radio("Moteur de rendu", ["Plotly (Interactif)", "Matplotlib (Statique)"])



    # Affichage du graphique choisi

    if engine == "Plotly (Interactif)":

        fig = px.bar(df, x=x_col, y=y_col, color=x_col, title="Rendu Plotly")

        st.plotly_chart(fig, use_container_width=True)

    else:

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.bar(df[x_col], df[y_col], color='skyblue')

        ax.set_title("Rendu Matplotlib")

        plt.xticks(rotation=45)

        st.pyplot(fig)
