import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="Mon Dashboard CSV", layout="wide")

st.title("📊 Analyseur de Fichiers CSV")
st.write("Chargez votre fichier pour visualiser les données instantanément.")

# Zone d'upload du fichier
uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="xls")

if uploaded_file is not None:
    # Lecture des données
    df = pd.read_csv(uploaded_file)
    
    # Affichage des statistiques rapides
    st.subheader("📋 Aperçu des données")
    st.dataframe(df.head())

    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Dimensions du tableau :**", df.shape)
    with col2:
        st.write("**Colonnes détectées :**", ", ".join(df.columns))

    st.divider()

    # Configuration du graphique
    st.subheader("📈 Visualisation personnalisée")
    
    columns = df.columns.tolist()
    
    c1, c2, c3 = st.columns(3)
    with c1:
        x_axis = st.selectbox("Axe X (Horizontal)", options=columns)
    with c2:
        y_axis = st.selectbox("Axe Y (Vertical)", options=columns)
    with c3:
        plot_type = st.selectbox("Type de graphique", ["Ligne", "Barres", "Points (Scatter)"])

    # Génération du graphique avec Plotly
    if plot_type == "Ligne":
        fig = px.line(df, x=x_axis, y=y_axis, title=f"{y_axis} en fonction de {x_axis}")
    elif plot_type == "Barres":
        fig = px.bar(df, x=x_axis, y=y_axis, title=f"Histogramme de {y_axis}")
    else:
        fig = px.scatter(df, x=x_axis, y=y_axis, title=f"Nuage de points : {y_axis} vs {x_axis}")

    st.plotly_chart(fig, use_container_width=True)

else:

    st.info("💡 En attente d'un fichier CSV...")
