import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import unicodedata

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="SKF Analyseur CSV/Excel", layout="wide")

# --- FONCTION POUR L'ANIMATION DE BACKGROUND ET LETTRES FLOTTANTES ---
def add_bg_animation():
    st.markdown(
        """
        <style>
        /* Animation du fond dégradé */
        .stApp {
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            overflow: hidden;
        }

        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Style des lettres SKF */
        .floating-letter {
            position: fixed;
            font-family: 'Arial Black', sans-serif;
            font-size: 80px;
            font-weight: bold;
            color: rgba(255, 255, 255, 0.15); /* Effet translucide comme de l'eau */
            user-select: none;
            z-index: -1; /* Derrière le contenu */
            pointer-events: none;
        }

        /* Animations de glissement "aquatique" */
        @keyframes water-glide {
            0% { transform: translate(0, 0) rotate(0deg); }
            33% { transform: translate(30px, 50px) rotate(5deg); }
            66% { transform: translate(-20px, 100px) rotate(-5deg); }
            100% { transform: translate(0, 0) rotate(0deg); }
        }

        /* Positionnement individuel et délais pour l'effet aléatoire */
        .letter-s { top: 15%; left: 10%; animation: water-glide 12s ease-in-out infinite; }
        .letter-k { top: 50%; left: 45%; animation: water-glide 18s ease-in-out infinite; animation-delay: 2s; }
        .letter-f { top: 75%; left: 80%; animation: water-glide 15s ease-in-out infinite; animation-delay: 4s; }

        /* Amélioration de la lisibilité des conteneurs */
        .stDataFrame, .stPlotlyChart, .stExpander, .stSelectbox, .stRadio, .stFileUploader {
            background-color: rgba(255, 255, 255, 0.85) !important;
            padding: 15px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        </style>

        <div class="floating-letter letter-s">S</div>
        <div class="floating-letter letter-k">K</div>
        <div class="floating-letter letter-f">F</div>
        """,
        unsafe_allow_html=True
    )

# Appel de l'animation
add_bg_animation()

# --- RESTE DU CODE (Inchangé) ---

def clean_column_names(df):
    new_columns = []
    for col in df.columns:
        nfkd_form = unicodedata.normalize('NFKD', str(col))
        clean_name = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
        new_columns.append(clean_name.lower().strip().replace(" ", "_"))
    df.columns = new_columns
    return df

st.title("📊 SKF - Analyseur de Données")
st.write("Format supportés : **CSV, XLSX, XLS**")

file = st.file_uploader("Déposez votre fichier ici", type=["csv", "xlsx", "xls"])

if file:
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    
    df = clean_column_names(df)
    st.success(f"Fichier '{file.name}' chargé avec succès !")
    
    with st.expander("👁️ Voir les données brutes"):
        st.dataframe(df)

    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        x_col = st.selectbox("Axe X", options=df.columns)
        y_col = st.selectbox("Axe Y", options=df.columns)
    
    with col2:
        engine = st.radio("Moteur de rendu", ["Plotly (Interactif)", "Matplotlib (Statique)"])

    if engine == "Plotly (Interactif)":
        fig = px.bar(df, x=x_col, y=y_col, color=x_col, title="Rendu Plotly")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(df[x_col], df[y_col], color='skyblue')
        ax.set_title("Rendu Matplotlib")
        fig.patch.set_alpha(0.0) # Fond transparent pour matplotlib
        plt.xticks(rotation=45)
        st.pyplot(fig)
