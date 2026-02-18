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

# 2. DESIGN GÉANT "S K F" EN ARRIÈRE-PLAN
st.markdown(
    """
    <style>
    /* On force l'arrière-plan global */
    .stApp {
        background-color: #FFFFFF !important;
    }

    /* Création du filigrane SKF géant */
    .stApp::before {
        content: "S K F";
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-15deg);
        font-size: 30vw; /* Taille immense */
        font-weight: 900;
        font-style: italic;
        color: rgba(0, 82, 147, 0.07) !important; /* Bleu SKF très léger */
        z-index: 0;
        white-space: nowrap;
        pointer-events: none;
        font-family: 'Arial Black', sans-serif;
    }

    /* On rend les blocs transparents pour voir le fond */
    [data-testid="stVerticalBlock"] > div {
        background-color: rgba(255, 255, 255, 0.6) !important;
        border-radius: 15px;
    }
    
    /* Titre stylé */
    h1 {
        color: #005293 !important;
        font-weight: 800;
        text-transform: uppercase;
        font-style: italic;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. INTERFACE UTILISATEUR
st.title("📊 SKF Dashboard : Analyseur Industriel")

file = st.file_uploader("📁 Déposez votre fichier Excel ou CSV", type=["csv", "xlsx", "xls"])

if file:
    # Gestion des moteurs de lecture
    if file.name.endswith('.xls'):
        df = pd.read_excel(file, engine='xlrd')
    elif file.name.endswith('.xlsx'):
        df = pd.read_excel(file, engine='openpyxl')
    else:
        df = pd.read_csv(file)
    
    df = clean_column_names(df)
    
    # Affichage des réglages
    st.subheader("⚙️ Configuration")
    x_col = st.pills("Axe X", options=df.columns, selection_mode="single", default=df.columns[0])
    y_col = st.pills("Axe Y", options=[c for c in df.columns if c != x_col], selection_mode="single", default=df.columns[1] if len(df.columns)>1 else df.columns[0])

    # Graphique Plotly aux couleurs SKF
    fig = px.bar(df, x=x_col, y=y_col, color_discrete_sequence=["#005293"])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
