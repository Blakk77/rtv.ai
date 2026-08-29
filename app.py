import os
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Rtv.ai", page_icon="🔧")

st.title("🔧 Rtv.ai - Expert Technique Automobile")
st.write("Base de données constructeur & Diagnostic intelligent rapide.")

# Configuration de l'API Gemini
if "GEMINI_API_KEY" in st.secrets:
  genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
elif "GEMINI_API_KEY" in os.environ:
  genai.configure(api_key=os.environ["GEMINI_API_KEY"])

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
modele_motorisation = st.text_input(
    "2. Précise le modèle et la motorisation (ex: W212 E350 V6...)"
)
probleme = st.text_area("3. Décris précisément le symptôme ou la panne :")

if st.button("Lancer l'analyse technique Autodata"):
  if modele_motorisation and probleme:
    # Utilisation d'une structure simple sans bloquer l'UI
    try:
      with st.spinner("Recherche dans la base technique en cours..."):
        # On utilise flash qui est ultra rapide (quelques secondes max)
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = (
            f"Agis en tant qu'expert technique automobile (type Autodata). "
            f"Véhicule : {marque_choisie} {modele_motorisation}. "
            f"Problème : {probleme}. "
            f"Donne rapidement : 1. Données techniques / couples clés. "
            f"2. Pannes connues sur ce modèle. 3. Procédure de diagnostic pas à pas."
        )

        response = model.generate_content(prompt)

        st.success("Diagnostic généré !")
        st.write(f"### 📚 Rapport Technique ({marque_choisie} - {modele_motorisation})")
        st.markdown(response.text)

    except Exception as e:
      st.error(
          "Erreur de connexion à l'IA. Vérifie bien que ta clé `GEMINI_API_KEY`"
          " est enregistrée dans les Settings > Secrets de Streamlit Cloud."
      )
  else:
    st.warning("Remplis bien le modèle et le problème stp.")
