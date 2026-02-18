import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import unicodedata

# Fonction pour nettoyer les noms de colonnes
def clean_column_names(df):
    new_columns = []
    for col in df.columns:
        nfkd_form = unicodedata.normalize('NFKD', str(col))
        clean_name = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
        new_columns.append(clean_name.lower().strip().replace(" ", "_"))
    df.columns = new_columns
    return df

st.set_page_config(page_title="Analyseur Pro CSV/Excel", layout="wide")

# --- AJOUT DU BACKGROUND AVEC LE LOGO SKF ---
# Remplace 'YOUR_SKF_LOGO_URL_HERE' par l'URL brute de ton logo SKF (depuis GitHub ou un hébergeur d'images)
SKF_LOGO_URL = "https://github.com/yussef-el/dashboard/blob/main/skf_logo.jpg" 

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url({SKF_LOGO_URL});
        background-attachment: fixed;
        background-size: 150px; /* Taille du logo */
        background-position: top 20px right 20px; /* Position en haut à droite */
        background-repeat: no-repeat; /* Ne pas répéter le logo */
        /* background-opacity: 0.2;  Pour rendre le logo un peu transparent si tu veux */
    }}
    /* Style pour rendre le contenu plus lisible au-dessus du logo si le logo est clair */
    .stApp > header {{
        background-color: rgba(255, 255, 255, 0.7); /* Fond semi-transparent pour le header */
    }}
    .stMarkdown, .stSubheader, .stText, .stButton, .stFileUploader, .stSelectbox, .stRadio, .stExpander, .stDataFrame, .stPlotlyChart, .stImage, .css-fg4lq4 {{
        background-color: rgba(255, 255, 255, 0.9); /* Fond blanc semi-transparent pour les éléments */
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }}
    .stRadio > div {{
        padding: 5px; /* Ajustement du padding pour les radios */
    }}
    </style>
    """,
    unsafe_allow_html=True
)
# --- FIN DE L'AJOUT DU BACKGROUND ---


st.title("📊 Analyseur de Données Multi-Formats")
st.write("Formats supportés : **CSV, XLSX, XLS**")

file = st.file_uploader("Déposez votre fichier ici", type=["csv", "xlsx", "xls"])

if file:
    if file.name.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(file)
    else:
        df = pd.read_csv(file)
    
    df = clean_column_names(df)
    st.success(f"Fichier '{file.name}' chargé et nettoyé !")
    
    with st.expander("👁️ Voir les données brutes"):
        st.dataframe(df)

    st.divider()
    
    st.subheader("⚙️ Configuration des axes")
    
    x_col = st.pills("Sélectionnez l'Axe X (Horizontal) :", options=df.columns, selection_mode="single", default=df.columns[0])
    
    y_options = [col for col in df.columns if col != x_col] # Exclut la colonne X pour l'axe Y
    if not y_options: # Si plus qu'une seule colonne, utilise la même
        y_options = [x_col]
        
    y_col = st.pills("Sélectionnez l'Axe Y (Vertical) :", options=y_options, selection_mode="single", default=y_options[0] if y_options else x_col)

    st.divider()

    engine = st.radio("Moteur de rendu", ["Plotly (Interactif)", "Matplotlib (Statique)"], horizontal=True)

    if x_col and y_col: 
        if engine == "Plotly (Interactif)":
            fig = px.bar(df, x=x_col, y=y_col, color=x_col, title=f"Analyse de {y_col} par {x_col}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(df[x_col], df[y_col], color='skyblue')
            ax.set_title(f"Rendu Matplotlib : {y_col}")
            plt.xticks(rotation=45)
            st.pyplot(fig)
    else:
        st.warning("Veuillez sélectionner une colonne pour chaque axe.")

