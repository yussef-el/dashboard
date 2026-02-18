import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import unicodedata

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Analyseur Pro CSV/Excel", layout="wide")

# --- FONCTION POUR L'ANIMATION DE BACKGROUND ---
def add_bg_animation():
    st.markdown(
        """
        <style>
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

        /* Amélioration de la lisibilité des cartes et conteneurs */
        .stDataFrame, .stPlotlyChart, .stExpander, .stSelectbox, .stRadio {
            background-color: rgba(255, 255, 255, 0.8) !important;
            padding: 10px;
            border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Appel de l'animation
add_bg_animation()

# --- RESTE DE TON CODE ---

def clean_column_names(df):
    new_columns = []
    for col in df.columns:
        nfkd_form = unicodedata.normalize('NFKD', str(col))
        clean_name = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
        new_columns.append(clean_name.lower().strip().replace(" ", "_"))
    df.columns = new_columns
    return df

st.title("📊 Analyseur de Données Multi-Formats")
st.write("Format supportés : **CSV, XLSX, XLS**")

file = st.file_uploader("Déposez votre fichier ici", type=["csv", "xlsx", "xls"])

if file:
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

    if engine == "Plotly (Interactif)":
        fig = px.bar(df, x=x_col, y=y_col, color=x_col, title="Rendu Plotly")
        # On rend le fond du graphique transparent pour voir l'animation derrière
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(df[x_col], df[y_col], color='skyblue')
        ax.set_title("Rendu Matplotlib")
        # Matplotlib gère moins bien la transparence native en Streamlit, 
        # mais on peut forcer le fond de la figure
        fig.patch.set_alpha(0.5) 
        plt.xticks(rotation=45)
        st.pyplot(fig)
