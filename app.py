import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import unicodedata

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="SKF Analyseur CSV/Excel", layout="wide")

# --- FONCTION POUR L'ANIMATION DE BACKGROUND ET LETTRES BLEUES ---
def add_bg_animation():
    st.markdown(
        """
        <style>
        /* 1. Animation du fond dégradé */
        .stApp {
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }

        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* 2. Style des lettres SKF en BLEU (Effet Eau) */
        .water-letter {
            position: fixed;
            font-family: 'Arial Black', sans-serif;
            font-size: 180px;
            font-weight: 900;
            /* Couleur BLEUE avec transparence pour l'effet liquide */
            color: rgba(0, 150, 255, 0.3); 
            text-shadow: 0 0 20px rgba(0, 100, 255, 0.2);
            z-index: 0;
            pointer-events: none;
            user-select: none;
        }

        /* 3. Animation de glissement fluide */
        @keyframes water-glide {
            0% { transform: translate(0, 0) rotate(0deg); }
            33% { transform: translate(60px, 40px) rotate(6deg); }
            66% { transform: translate(-40px, 120px) rotate(-4deg); }
            100% { transform: translate(0, 0) rotate(0deg); }
        }

        .letter-s { top: 10%; left: 8%; animation: water-glide 14s infinite ease-in-out; }
        .letter-k { top: 40%; left: 45%; animation: water-glide 18s infinite ease-in-out; animation-delay: 2s; }
        .letter-f { bottom: 15%; right: 10%; animation: water-glide 16s infinite ease-in-out; animation-delay: 4s; }

        /* 4. Conteneurs Streamlit (Blancs semi-transparents) */
        .stDataFrame, .stPlotlyChart, .stExpander, .stSelectbox, .stRadio, .stFileUploader {
            background-color: rgba(255, 255, 255, 0.9) !important;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            position: relative;
            z-index: 10;
        }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>

        <div class="water-letter letter-s">S</div>
        <div class="water-letter letter-k">K</div>
        <div class="water-letter letter-f">F</div>
        """,
        unsafe_allow_html=True
    )

add_bg_animation()

# --- FONCTIONS DE TRAITEMENT ---
def clean_column_names(df):
    new_columns = []
    for col in df.columns:
        nfkd_form = unicodedata.normalize('NFKD', str(col))
        clean_name = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
        new_columns.append(clean_name.lower().strip().replace(" ", "_"))
    df.columns = new_columns
    return df

# --- INTERFACE ---
st.title("📊 SKF - Analyseur de Données")
st.markdown("### Les lettres **S, K, F** glissent désormais en bleu sur le fond.")

file = st.file_uploader("📂 Déposez votre fichier (CSV ou Excel)", type=["csv", "xlsx", "xls"])

if file:
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    
    df = clean_column_names(df)
    st.success(f"✅ Fichier '{file.name}' prêt !")
    
    with st.expander("👁️ Aperçu des données"):
        st.dataframe(df, use_container_width=True)

    st.divider()
    
    c1, c2 = st.columns(2)
    with c1:
        x_col = st.selectbox("Axe X", options=df.columns)
        y_col = st.selectbox("Axe Y", options=df.columns)
    with c2:
        engine = st.radio("Style de graphique", ["Plotly (Interactif)", "Matplotlib (Statique)"])

    if engine == "Plotly (Interactif)":
        fig = px.bar(df, x=x_col, y=y_col, color=x_col, template="plotly_white")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig, ax = plt.subplots()
        ax.bar(df[x_col], df[y_col], color='#0096FF')
        plt.xticks(rotation=45)
        fig.patch.set_alpha(0.0)
        st.pyplot(fig)
