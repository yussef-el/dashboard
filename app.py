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

        /* 2. Style des lettres SKF (Effet Eau) */
        .water-letter {
            position: fixed;
            font-family: 'Arial Black', sans-serif;
            font-size: 180px; /* Taille augmentée pour plus d'impact */
            font-weight: 900;
            color: rgba(255, 255, 255, 0.25); /* Opacité ajustée pour être visible */
            z-index: 0; /* Placé derrière les widgets mais devant le fond */
            pointer-events: none; /* Ne bloque pas les clics de souris */
            user-select: none;
        }

        /* 3. Animation de glissement fluide */
        @keyframes water-glide {
            0% { transform: translate(0, 0) rotate(0deg); }
            33% { transform: translate(50px, 80px) rotate(8deg); }
            66% { transform: translate(-30px, 150px) rotate(-5deg); }
            100% { transform: translate(0, 0) rotate(0deg); }
        }

        /* Positions spécifiques et vitesses différentes pour chaque lettre */
        .letter-s { top: 5%; left: 5%; animation: water-glide 15s infinite ease-in-out; }
        .letter-k { top: 35%; left: 40%; animation: water-glide 20s infinite ease-in-out; animation-delay: 2s; }
        .letter-f { bottom: 10%; right: 10%; animation: water-glide 18s infinite ease-in-out; animation-delay: 4s; }

        /* 4. Amélioration de la lisibilité des conteneurs Streamlit */
        .stDataFrame, .stPlotlyChart, .stExpander, .stSelectbox, .stRadio, .stFileUploader {
            background-color: rgba(255, 255, 255, 0.9) !important;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            position: relative;
            z-index: 10; /* Force le passage AU-DESSUS des lettres */
        }
        
        /* Cacher le menu Streamlit et le footer pour un look plus clean */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>

        <div class="water-letter letter-s">S</div>
        <div class="water-letter letter-k">K</div>
        <div class="water-letter letter-f">F</div>
        """,
        unsafe_allow_html=True
    )

# Appel de l'animation au chargement
add_bg_animation()

# --- LOGIQUE DE NETTOYAGE DES DONNÉES ---
def clean_column_names(df):
    new_columns = []
    for col in df.columns:
        nfkd_form = unicodedata.normalize('NFKD', str(col))
        clean_name = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
        new_columns.append(clean_name.lower().strip().replace(" ", "_"))
    df.columns = new_columns
    return df

# --- INTERFACE UTILISATEUR ---
st.title("📊 SKF - Analyseur de Données")
st.markdown("### Visualisation intelligente pour fichiers **CSV** et **Excel**")

file = st.file_uploader("📂 Déposez votre fichier ici", type=["csv", "xlsx", "xls"])

if file:
    # Chargement des données
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    
    # Nettoyage des colonnes
    df = clean_column_names(df)
    st.success(f"✅ Fichier '{file.name}' chargé et nettoyé avec succès !")
    
    # Section visualisation brute
    with st.expander("👁️ Consulter le tableau des données"):
        st.dataframe(df, use_container_width=True)

    st.divider()
    
    # Configuration des graphiques
    col1, col2 = st.columns(2)
    with col1:
        x_col = st.selectbox("Sélectionnez l'axe X (Abscisses)", options=df.columns)
        y_col = st.selectbox("Sélectionnez l'axe Y (Ordonnées)", options=df.columns)
    
    with col2:
        engine = st.radio("Moteur de rendu graphique", ["Plotly (Interactif)", "Matplotlib (Statique)"])

    # Affichage du graphique
    if engine == "Plotly (Interactif)":
        fig = px.bar(df, x=x_col, y=y_col, color=x_col, 
                     title=f"Répartition de {y_col} par {x_col}",
                     template="plotly_white")
        # Transparence du graphique pour voir le fond glisser derrière
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(df[x_col], df[y_col], color='#23a6d5')
        ax.set_title(f"Analyse {x_col} / {y_col}")
        plt.xticks(rotation=45)
        # On rend le fond de la figure matplotlib transparent
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')
        st.pyplot(fig)

else:
    st.info("💡 En attente d'un fichier pour commencer l'analyse.")
