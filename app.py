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

# --- DESIGN S K F (BODONI MT BLACK - SANS ITALIQUE) ---
st.markdown(
    """
    <style>
    /* Configuration du fond sombre */
    .stApp {
        background-color: #0E1117 !important;
    }

    /* Filigrane S K F Géant (Droit/Normal) */
    .stApp::before {
        content: "S K F";
        position: fixed;
        top: 55%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 35vw; 
        font-weight: 900;
        font-style: normal; /* Italique supprimé ici */
        font-family: 'Bodoni MT Black', 'Bodoni MT', serif;
        color: rgba(255, 255, 255, 0.12) !important; 
        z-index: 0;
        white-space: nowrap;
        pointer-events: none;
    }

    /* Rendre le contenu lisible par dessus le fond */
    [data-testid="stVerticalBlock"] > div {
        background-color: rgba(25, 30, 41, 0.75) !important;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    h1, h2, h3, p, label {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 Analyseur de Données Multi-Formats")
st.write("Format supportés : **CSV, XLSX, XLS**")

# Upload du fichier
file = st.file_uploader("Déposez votre fichier ici", type=["csv", "xlsx", "xls"])

if file:
    # Lecture selon l'extension
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        # Pandas choisit le moteur (openpyxl/xlrd) automatiquement
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
        # Fond transparent pour le graphique pour voir le filigrane derrière
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(df[x_col], df[y_col], color='#005293') # Bleu SKF
        ax.set_title("Rendu Matplotlib")
        plt.xticks(rotation=45)
        st.pyplot(fig)
