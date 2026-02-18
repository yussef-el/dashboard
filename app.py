import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import unicodedata

# 1. Fonction pour nettoyer les noms de colonnes
def clean_column_names(df):
    new_columns = []
    for col in df.columns:
        nfkd_form = unicodedata.normalize('NFKD', str(col))
        clean_name = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
        new_columns.append(clean_name.lower().strip().replace(" ", "_"))
    df.columns = new_columns
    return df

st.set_page_config(page_title="Analyseur Pro SKF", layout="wide")

# 2. DESIGN : FOND BLANC + LETTRES BLEU FONCÉ (BODONI MT BLACK)
st.markdown(
    """
    <style>
    /* Fond de l'application en blanc */
    .stApp {
        background-color: #FFFFFF !important;
    }

    /* Filigrane S K F Géant en BLEU FONCÉ */
    .stApp::before {
        content: "S K F";
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 35vw; 
        font-weight: 900;
        font-style: normal;
        font-family: 'Bodoni MT Black', 'Bodoni MT', serif;
        /* Bleu foncé SKF avec opacité légère pour le fond blanc */
        color: rgba(0, 82, 147, 0.08) !important; 
        z-index: 0;
        white-space: nowrap;
        pointer-events: none;
    }

    /* Rendre les blocs légèrement opaques pour la lisibilité */
    [data-testid="stVerticalBlock"] > div {
        background-color: rgba(255, 255, 255, 0.7) !important;
        border-radius: 12px;
        padding: 15px;
    }

    /* Couleurs de texte pour fond blanc */
    h1, h2, h3, p, label {
        color: #005293 !important; /* Bleu SKF pour le texte */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. INTERFACE
st.title("📊 Analyseur de Données Multi-Formats")
st.write("Format supportés : **CSV, XLSX, XLS**")

file = st.file_uploader("Déposez votre fichier ici", type=["csv", "xlsx", "xls"])

if file:
    # Lecture selon l'extension
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    
    df = clean_column_names(df)
    st.success(f"Fichier '{file.name}' chargé et nettoyé !")
    
    with st.expander("👁️ Voir les données brutes"):
        st.dataframe(df)

    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        x_col = st.selectbox("Axe X", options=df.columns)
        y_col = st.selectbox("Axe Y", options=df.columns)
    
    with col2:
        engine = st.radio("Moteur de rendu", ["Plotly (Interactif)", "Matplotlib (Statique)"])

    # Graphiques
    if engine == "Plotly (Interactif)":
        fig = px.bar(df, x=x_col, y=y_col, color=x_col, title="Rendu Plotly")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(df[x_col], df[y_col], color='#005293') 
        ax.set_title("Rendu Matplotlib")
        plt.xticks(rotation=45)
        st.pyplot(fig)
