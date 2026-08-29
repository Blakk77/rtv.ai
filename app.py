import os
import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="Rtv.ai - Expert Atelier Pro", page_icon="🔧", layout="centered"
)

# Design CSS pro type dark-mode atelier
st.markdown(
    """
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem;
        border: none;
    }
    .stButton>button:hover { background-color: #ff2b2b; color: white; }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    "# 🔧 Rtv.ai <span style='color:#ff4b4b;'>Expert Atelier</span>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='color: #8b949e;'>Module de diagnostic technique intelligent"
    " interconnecté.</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Configuration de la clé API Gemini (via Streamlit Secrets ou variable d'env)
api_key = None
if "GEMINI_API_KEY" in st.secrets:
  api_key = st.secrets["GEMINI_API_KEY"]
elif "GEMINI_API_KEY" in os.environ:
  api_key = os.environ["GEMINI_API_KEY"]

if api_key:
  genai.configure(api_key=api_key)

# Formulaire d'entrée
st.markdown("### 📋 1. Identification du Véhicule")
marques = [
    "Mercedes-Benz",
    "BMW",
    "Audi",
    "Volkswagen",
    "Renault",
    "Peugeot",
    "Autre",
]
col1, col2 = st.columns(2)
with col1:
  marque_choisie = st.selectbox("Marque constructeur", marques)
with col2:
  modele_motorisation = st.text_input(
      "Modèle & Motorisation",
      placeholder="ex: W212 E350 V6 CDI 265ch",
  )

st.markdown("### 🔍 2. Symptôme / Panne constatée")
probleme = st.text_area(
    "Description précise du problème",
    placeholder="ex: bruit de fuite aux injecteurs, claquement à froid, perte de puissance...",
    height=100,
)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Lancer l'analyse technique approfondie"):
  if not api_key:
    st.error(
        "❌ Clé API manquante ! Ajoute ta `GEMINI_API_KEY` dans les Secrets de"
        " ton application Streamlit Cloud."
    )
  elif modele_motorisation and probleme:
    try:
      with st.spinner(
          "Interrogation des bases de données techniques et analyse en"
          " cours..."
      ):
        # Utilisation du modèle rapide et ultra performant
        model = genai.GenerativeModel("gemini-2.5-flash")

        # Prompt ultra-cadré pour forcer l'IA à répondre précisément au cas exact
        prompt = f"""
        Agis en tant qu'expert technique automobile de premier plan (type ingénieur diagnostic / Autodata / ElsaWin).
        Véhicule concerné : {marque_choisie} - {modele_motorisation}.
        Symptôme exact décrit par le mécanicien : "{probleme}".

        Analyse ce problème spécifique en te basant sur les pannes connues réelles de cette motorisation. Ne réponds pas de manière générique, cible précisément le symptôme indiqué (injecteurs, turbo, bruits, etc.).

        Structure ta réponse en clair avec ces sections exactes en Markdown :
        1. ⚙️ **Analyse ciblée du symptôme** (pourquoi ce problème survient précisément sur ce modèle).
        2. ⚠️ **Causes principales & Pièces en cause** (liste claire des causes probables par ordre de probabilité).
        3. 🛠️ **Procédure de diagnostic et de résolution pas à pas** (méthode d'atelier détaillée pour réparer).
        4. 🔩 **Données techniques utiles** (couples de serrage, normes ou références constructeur si applicables).
        """

        response = model.generate_content(prompt)

        st.success("✅ Rapport d'analyse technique généré avec succès !")
        st.markdown("---")
        st.markdown(
            f"## 📊 Rapport d'Atelier : {marque_choisie} ({modele_motorisation})"
        )
        st.markdown(response.text)

    except Exception as e:
      st.error(f"Une erreur est survenue lors de l'appel à l'IA : {e}")
  else:
    st.warning("⚠️ Merci de remplir le modèle/motorisation et la description.")
