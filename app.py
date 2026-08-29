import os
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Rtv.ai", page_icon="🔧")

st.title("🔧 Rtv.ai - Expert Technique Automobile")
st.write("Base de données constructeur & Diagnostic intelligent dynamique.")

# Configuration de l'API Gemini (utilise la clé secrète configurée dans Streamlit Cloud)
if "GEMINI_API_KEY" in st.secrets:
  genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
  # Fallback si test en local avec variable d'environnement
  if "GEMINI_API_KEY" in os.environ:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Étape 1 : Choix de la marque
marques = [
    "Mercedes-Benz",
    "BMW",
    "Audi",
    "Volkswagen",
    "Renault",
    "Peugeot",
    "Autre",
]
marque_choisie = st.selectbox("1. Choisis la marque du véhicule :", marques)

# Étape 2 : Saisie du modèle et du moteur
modele_motorisation = st.text_input(
    "2. Précise le modèle et la motorisation (ex: W212 E350 V6, Série 3 E90...)"
)

# Étape 3 : Description du problème
probleme = st.text_area("3. Décris précisément le symptôme ou la panne :")

if st.button("Lancer l'analyse technique Autodata"):
  if modele_motorisation and probleme:
    with st.spinner(
        "Interrogation des bases de données techniques et analyse en"
        " cours..."
    ):
      try:
        # Utilisation du modèle Gemini pour générer une réponse technique précise
        model = genai.GenerativeModel("gemini-1.5-pro")
        prompt = (
            f"Agis en tant qu'expert technique automobile et base de données de type Autodata. "
            f"Véhicule concerné : {marque_choisie} {modele_motorisation}. "
            f"Problème / Symptôme décrit : {probleme}. "
            f"Fournis une réponse structurée comprenant :\n"
            f"1. Les données techniques constructeur pertinentes (couples de serrage, points de contrôle clés ou schémas si applicable).\n"
            f"2. Les pannes connues répertoriées sur cette motorisation exacte.\n"
            f"3. La procédure de diagnostic pas à pas pour résoudre ce problème précis."
        )

        response = model.generate_content(prompt)

        st.success("Diagnostic technique généré avec succès !")
        st.write(f"### 📚 Rapport Technique ({marque_choisie} - {modele_motorisation})")
        st.markdown(response.text)

      except Exception as e:
        st.error(
            "Oups, la clé API Gemini n'est pas encore configurée dans les"
            " secrets Streamlit Cloud."
        )
        st.info(
            "Pour activer l'IA, ajoute ta clé `GEMINI_API_KEY` dans les"
            " réglages de ton app sur Streamlit Cloud (Settings > Secrets)."
        )
  else:
    st.warning("Remplis bien le modèle et le problème stp.")
