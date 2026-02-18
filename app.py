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

st.set_page_config(page_title="SKF Data Dashboard", layout="wide")

# 2. DESIGN : LETTRES S K F EN BACKGROUND GÉANT
st.markdown(
    """
    <style>
    /* Création du texte géant en arrière-plan */
    .stApp::before {
        content: "S K F";
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-10deg);
        font-size: 25vw; /* Occupe 25% de la largeur de l'écran */
        font-weight: 900;
        font-style: italic;
        color: rgba(0, 82, 147, 0.05); /* Bleu SKF très clair pour ne pas gêner la lecture */
        z-index: -1;
        white-space: nowrap;
        font-family: 'Arial Black', sans-serif;
    }

    /* Amélioration des blocs de contenu */
    [data-testid="stVerticalBlock"] > div:has(div.stFrame) {
        background: rgba(255, 255, 255, 0.8);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(0, 82, 147, 0.1);
        box-shadow: 0 8px 32px rgba(0, 82, 147, 0.05);
    }
    
    h1 {
        color: #005293;
        border-bottom: 3px solid #005293;
        padding-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. INTERFACE UTILISATEUR
st.title("📊 SKF Dashboard : Analyseur Industriel")

file = st.file_uploader("📁 Déposez votre fichier Excel ou CSV", type=["csv", "xlsx", "xls"])

if file:
    # Gestion des formats (Correction pour les anciens .xls)
    if file.name.endswith('.xls'):
        df = pd.read_excel(file, engine='xlrd')
    elif file.name.endswith('.xlsx'):
        df = pd.read_excel(file, engine='openpyxl')
    else:
        df = pd.read_csv(file)
    
    df = clean_column_names(df)
    st.success(f"✅ Analyse du fichier : {file.name}")
    
    with st.expander("🔍 Explorer les données brutes"):
        st.dataframe(df, use_container_width=True)

    st.divider()
    
    # 4. CONFIGURATION DES AXES (BOUTONS PILLS)
    st.subheader("⚙️ Paramètres du Graphique")
    
    x_col = st.pills("Axe Horizontal (X)", options=df.columns, selection_mode="single", default=df.columns[0])
    
    # On filtre pour ne pas avoir X dans les choix de Y
    y_choices = [c for c in df.columns if c != x_col]
    y_col = st.pills("Axe Vertical (Y)", options=y_choices, selection_mode="single", default=y_choices[0] if y_choices else df.columns[0])

    engine = st.radio("Style de rendu :", ["Plotly (Interactif)", "Matplotlib (Rapport)"], horizontal=True)

    # 5. GÉNÉRATION DU GRAPHIQUE
    if x_col and y_col:
        if engine == "Plotly (Interactif)":
            fig = px.bar(df, x=x_col, y=y_col, color=x_col, 
                         template="plotly_white",
                         color_discrete_sequence=["#005293", "#F2F2F2"]) # Palette aux couleurs SKF
            st.plotly_chart(fig, use_container_width=True)
        else:
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.bar(df[x_col], df[y_col], color='#005293')
            ax.set_title(f"Analyse : {y_col}", fontstyle='italic', color='#005293')
            plt.xticks(rotation=45)
            st.pyplot(fig)
