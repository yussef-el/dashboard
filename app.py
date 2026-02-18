import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import unicodedata

# 1. NETTOYAGE DES DONNÉES
def clean_column_names(df):
    new_columns = []
    for col in df.columns:
        nfkd_form = unicodedata.normalize('NFKD', str(col))
        clean_name = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
        new_columns.append(clean_name.lower().strip().replace(" ", "_"))
    df.columns = new_columns
    return df

st.set_page_config(page_title="SKF Industrial Dashboard", layout="wide")

# 2. DESIGN DARK THEME + LETTRES GÉANTES BLANCHES
st.markdown(
    """
    <style>
    /* Force le fond sombre sur toute l'application */
    .stApp {
        background-color: #0E1117 !important;
    }

    /* Création des lettres S K F géantes en BLANC, GRAS et ITALIQUE */
    .stApp::before {
        content: "S K F";
        position: fixed;
        top: 55%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-10deg);
        font-size: 35vw; /* Taille immense */
        font-weight: 900; /* Très Gras */
        font-style: italic; /* Italique */
        color: rgba(255, 255, 255, 0.12) !important; /* Blanc avec légère transparence pour le style */
        z-index: 0;
        white-space: nowrap;
        pointer-events: none;
        font-family: 'Arial Black', sans-serif;
        letter-spacing: -1vw;
    }

    /* Rend les blocs de contenu semi-transparents pour laisser passer le fond */
    [data-testid="stVerticalBlock"] > div {
        background-color: rgba(25, 30, 41, 0.7) !important;
        padding: 15px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Titre en blanc brillant */
    h1 {
        color: #FFFFFF !important;
        font-weight: 800;
        font-style: italic;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    /* Ajustement des textes secondaires */
    .stMarkdown, p, label {
        color: #E0E0E0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. INTERFACE UTILISATEUR
st.title("📊 SKF Dashboard : Analyseur Industriel")

file = st.file_uploader("📁 Déposez votre fichier Excel ou CSV", type=["csv", "xlsx", "xls"])

if file:
    # Lecture des fichiers
    try:
        if file.name.endswith('.xls'):
            df = pd.read_excel(file, engine='xlrd')
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file, engine='openpyxl')
        else:
            df = pd.read_csv(file)
        
        df = clean_column_names(df)
        st.success(f"✅ Fichier chargé avec succès")
        
        # Configuration des graphiques
        st.divider()
        col_controls = st.container()
        with col_controls:
            x_col = st.pills("Axe X (Horizontal)", options=df.columns, selection_mode="single", default=df.columns[0])
            y_col = st.pills("Axe Y (Valeurs)", options=[c for c in df.columns if c != x_col], selection_mode="single", default=df.columns[1] if len(df.columns)>1 else df.columns[0])

        # Graphique Plotly avec thème sombre
        if x_col and y_col:
            fig = px.bar(df, x=x_col, y=y_col, color_discrete_sequence=["#005293"])
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)',
                font_color="white",
                title_font_size=20
            )
            st.plotly_chart(fig, use_container_width=True)
            
    except Exception as e:
        st.error(f"Erreur lors de la lecture : {e}")
