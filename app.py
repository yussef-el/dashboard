import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import unicodedata

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="SKF Analyseur CSV/Excel", layout="wide")

# --- FONCTION POUR LE DARK THEME ET LES LETTRES FLOTTANTES ---
def add_custom_style():
    st.markdown(
        """
        <style>
        /* 1. Fond Dark Theme Fixe */
        .stApp {
            background-color: #0E1117; /* Noir bleuté standard Streamlit Dark */
            background-attachment: fixed;
        }

        /* 2. Style des lettres SKF en BLEU */
        .water-letter {
            position: fixed;
            font-family: 'Arial Black', sans-serif;
            font-size: 200px;
            font-weight: 900;
            color: rgba(0, 120, 255, 0.2); /* Bleu aquatique transparent */
            text-shadow: 0 0 15px rgba(0, 120, 255, 0.1);
            z-index: 0;
            pointer-events: none;
            user-select: none;
        }

        /* 3. Animation de glissement fluide (effet eau) */
        @keyframes water-glide {
            0% { transform: translate(0, 0) rotate(0deg); }
            50% { transform: translate(80px, 40px) rotate(5deg); }
            100% { transform: translate(0, 0) rotate(0deg); }
        }

        .letter-s { top: 10%; left: 10%; animation: water-glide 12s infinite ease-in-out; }
        .letter-k { top: 45%; left: 40%; animation: water-glide 16s infinite ease-in-out; animation-delay: 1s; }
        .letter-f { bottom: 15%; right: 15%; animation: water-glide 14s infinite ease-in-out; animation-delay: 2s; }

        /* 4. Adaptation des conteneurs pour le Dark Theme */
        .stDataFrame, .stPlotlyChart, .stExpander, .stSelectbox, .stRadio, .stFileUploader {
            background-color: rgba(38, 39, 48, 0.8) !important; /* Gris foncé transparent */
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 15px;
            position: relative;
            z-index: 10;
        }

        /* Texte en blanc pour le mode sombre */
        h1, h2, h3, p, label {
            color: #FFFFFF !important;
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

add_custom_style()

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
st.write("Mode sombre activé avec lettres bleues flottantes.")

file = st.file_uploader("📂 Déposez votre fichier (CSV ou Excel)", type=["csv", "xlsx", "xls"])

if file:
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    
    df = clean_column_names(df)
    st.success(f"✅ Données de '{file.name}' prêtes !")
    
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
        # Utilisation du template sombre pour Plotly
        fig = px.bar(df, x=x_col, y=y_col, color=x_col, template="plotly_dark")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Style sombre pour Matplotlib
        plt.style.use('dark_background')
        fig, ax = plt.subplots()
        ax.bar(df[x_col], df[y_col], color='#0078FF')
        plt.xticks(rotation=45)
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')
        st.pyplot(fig)
