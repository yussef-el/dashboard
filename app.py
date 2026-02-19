import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import unicodedata

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="SKF Analyseur CSV/Excel", layout="wide")

# --- FONCTION POUR LE STYLE DARK ET ANIMATION PLEIN ÉCRAN ---
def add_custom_style():
    st.markdown(
        """
        <style>
        /* 1. Fond Dark Theme Fixe */
        .stApp {
            background-color: #0E1117;
            overflow: hidden; /* Évite les barres de défilement dues aux lettres */
        }

        /* 2. Style des lettres SKF en BLEU */
        .water-letter {
            position: fixed;
            font-family: 'Arial Black', sans-serif;
            font-size: 250px; /* Taille augmentée */
            font-weight: 900;
            color: rgba(0, 120, 255, 0.15); /* Bleu subtil */
            z-index: 0;
            pointer-events: none;
            user-select: none;
            white-space: nowrap;
        }

        /* 3. Animation de glissement sur TOUT l'écran */
        @keyframes drift {
            0% { transform: translate(-20vw, -20vh) rotate(0deg); }
            25% { transform: translate(60vw, 10vh) rotate(90deg); }
            50% { transform: translate(80vw, 60vh) rotate(180deg); }
            75% { transform: translate(10vw, 80vh) rotate(270deg); }
            100% { transform: translate(-20vw, -20vh) rotate(360deg); }
        }

        /* Délais et durées différents pour chaque lettre pour éviter l'effet "bloc" */
        .letter-s { animation: drift 25s linear infinite; }
        .letter-k { animation: drift 35s linear infinite reverse; animation-delay: -5s; }
        .letter-f { animation: drift 30s linear infinite; animation-delay: -10s; }

        /* 4. Adaptation des conteneurs pour le Dark Theme */
        .stDataFrame, .stPlotlyChart, .stExpander, .stSelectbox, .stRadio, .stFileUploader {
            background-color: rgba(38, 39, 48, 0.85) !important;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 15px;
            position: relative;
            z-index: 10;
            backdrop-filter: blur(5px); /* Effet de flou sous les boites */
        }

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

# --- LOGIQUE DE NETTOYAGE ---
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
st.write("Les lettres parcourent maintenant l'intégralité de l'écran.")

file = st.file_uploader("📂 Déposez votre fichier (CSV ou Excel)", type=["csv", "xlsx", "xls"])

if file:
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    
    df = clean_column_names(df)
    st.success(f"✅ Données chargées")
    
    with st.expander("👁️ Aperçu"):
        st.dataframe(df, use_container_width=True)

    st.divider()
    
    c1, c2 = st.columns(2)
    with c1:
        x_col = st.selectbox("Axe X", options=df.columns)
        y_col = st.selectbox("Axe Y", options=df.columns)
    with c2:
        engine = st.radio("Moteur graphique", ["Plotly (Interactif)", "Matplotlib (Statique)"])

    if engine == "Plotly (Interactif)":
        fig = px.bar(df, x=x_col, y=y_col, color=x_col, template="plotly_dark")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    else:
        plt.style.use('dark_background')
        fig, ax = plt.subplots()
        ax.bar(df[x_col], df[y_col], color='#0078FF')
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')
        st.pyplot(fig)
