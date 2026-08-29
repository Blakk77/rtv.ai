import os
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Rtv.ai", page_icon="🔧", layout="centered")

st.markdown(
    """
    <style>
    /* Dégradé bien visible et stylé */
    .stApp {
        background: linear-gradient(145deg, #0b0f19 0%, #1e2538 40%, #0d121c 100%);
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem;
        border: none;
        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.3);
    }
    .stButton>button:hover { 
        background-color: #ff2b2b; 
        color: white; 
        box-shadow: 0 6px 16px rgba(255, 43, 43, 0.5);
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown("# 🔧 Rtv.ai <span style='color:#ff4b4b;'>Expert Méchanique</span>", unsafe_allow_html=True)

api_key = None
if "GEMINI_API_KEY" in st.secrets:
  api_key = st.secrets["GEMINI_API_KEY"]
elif "GEMINI_API_KEY" in os.environ:
  api_key = os.environ["GEMINI_API_KEY"]

if api_key:
  genai.configure(api_key=api_key)

col1, col2 = st.columns(2)
with col1:
  marque_choisie = st.selectbox(
      "Marque",
      ["Mercedes-Benz", "BMW", "Audi", "Volkswagen", "Renault", "Peugeot"],
  )
with col2:
  modele = st.text_input("Modèle & Motorisation", placeholder="ex: W212 E350 V6")

probleme = st.text_input("Symptôme précis", placeholder="ex: bruit injecteur")

if st.button("Lancer le diagnostic rapide"):
  if not api_key:
    st.error("❌ Clé API manquante dans les secrets.")
  elif modele and probleme:
    try:
      with st.spinner("Analyse..."):
        model = genai.GenerativeModel("gemini-3.6-flash")

        prompt = f"""
        Expert mécanicien. Véhicule: {marque_choisie} {modele}. Symptôme: "{probleme}".
        Donne une réponse ultra-courte, sans phrase de politesse, style mécano pressé.

        1. Coupable numéro 1 (La pièce précise en 1 ligne).
        2. Test rapide (Comment vérifier en 1 minute).
        3. Serrage / Référence (Si applicable).
        """

        response = model.generate_content(prompt)

        st.markdown("---")
        st.markdown(
            f"### 📊 Résultat : {marque_choisie} ({modele}) - {probleme}"
        )
        st.markdown(response.text)

    except Exception as e:
      st.error(f"Erreur : {e}")
  else:
    st.warning("⚠️ Remplis tous les champs.")
