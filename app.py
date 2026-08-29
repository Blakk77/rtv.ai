import os
import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="Rtv.ai - Expert Atelier Pro", page_icon="🔧", layout="centered"
)

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

api_key = None
if "GEMINI_API_KEY" in st.secrets:
  api_key = st.secrets["GEMINI_API_KEY"]
elif "GEMINI_API_KEY" in os.environ:
  api_key = os.environ["GEMINI_API_KEY"]

if api_key:
  genai.configure(api_key=api_key)

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
    placeholder="ex: bruit d'injecteur, perte de puissance...",
    height=100,
)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Lancer l'analyse technique approfondie"):
  if not api_key:
    st.error("❌ Clé API manquante dans les secrets Streamlit.")
  elif modele_motorisation and probleme:
    try:
      with st.spinner("Analyse technique en cours..."):
        # Modèle exigé par l'API
        model = genai.GenerativeModel("gemini-3.6-flash")

        prompt = f"""
        Agis en tant qu'expert technique automobile de premier plan (ingénieur diagnostic / Autodata).
        Véhicule : {marque_choisie} - {modele_motorisation}.
        Symptôme : "{probleme}".

        Analyse ce problème précisément en te basant sur les pannes réelles de cette motorisation. 

        Structure ta réponse en clair avec ces sections exactes en Markdown :
        1. ⚙️ **Analyse ciblée du symptôme**
        2. ⚠️ **Causes principales & Pièces en cause**
        3. 🛠️ **Procédure de diagnostic et de résolution pas à pas**
        4. 🔩 **Données techniques utiles** (couples de serrage, normes...)
        """

        response = model.generate_content(prompt)

        st.success("✅ Rapport généré avec succès !")
        st.markdown("---")
        st.markdown(
            f"## 📊 Rapport d'Atelier : {marque_choisie} ({modele_motorisation})"
        )
        st.markdown(response.text)

    except Exception as e:
      st.error(f"Erreur technique : {e}")
  else:
    st.warning("⚠️ Merci de remplir tous les champs.")
