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

# 2. DESIGN : LOGO EN ARRIÈRE-PLAN (CSS)
# REMPLACE CETTE URL par le lien vers ton fichier .jpg sur GitHub
LOGO_URL = "https://github.com/yussef-el/dashboard/blob/main/skf_logo.jpg"

st.markdown(
    f"""
    <style>
    /* Configuration de l'image de fond */
    .stApp {{
        background-image: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), url("{LOGO_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Design des blocs pour qu'ils soient lisibles et élégants */
    [data-testid="stVerticalBlock"] > div:has(div.stFrame) {{
        background: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    
    /* Style spécifique pour les titres */
    h1, h2, h3 {{
        color: #005293; /* Bleu SKF */
        font-family: 'Arial', sans-serif;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# 3. INTERFACE UTILISATEUR
st.title("📊 SKF Dashboard : Analyseur Multi-Formats")

file = st.file_uploader("📁 Chargez votre fichier (CSV, XLSX, XLS)", type=["csv", "xlsx", "xls"])

if file:
    # Gestion des formats
    if file.name.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(file)
    else:
        df = pd.read_csv(file)
    
    df = clean_column_names(df)
    st.success(f"✅ Fichier '{file.name}' prêt pour l'analyse")
    
    with st.expander("🔍 Aperçu des données"):
        st.dataframe(df, use_container_width=True)

    st.divider()
    
    # 4. CONFIGURATION DES AXES AVEC LES BOUTONS (PILLS)
    st.subheader("⚙️ Configuration du Graphique")
    
    col_x, col_y = st.columns(2)
    
    with col_x:
        x_col = st.pills("Choisir l'Axe X", options=df.columns, selection_mode="single", default=df.columns[0])
    
    with col_y:
        y_options = [c for c in df.columns if c != x_col]
        y_col = st.pills("Choisir l'Axe Y", options=y_options, selection_mode="single", default=y_options[0] if y_options else df.columns[0])

    engine = st.radio("Moteur de rendu :", ["Plotly (Dynamique)", "Matplotlib (Fixe)"], horizontal=True)

    # 5. Rendu du graphique
    if x_col and y_col:
        if engine == "Plotly (Dynamique)":
            fig = px.bar(df, x=x_col, y=y_col, color=x_col, 
                         template="plotly_white", 
                         title=f"Distribution de {y_col} par {x_col}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.bar(df[x_col], df[y_col], color='#005293') # Couleur SKF
            ax.set_title(f"Rendu Statique : {y_col}")
            plt.xticks(rotation=45)
            st.pyplot(fig)

