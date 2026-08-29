import json
import os
import google.generativeai as genai
import streamlit as st

st.set_page_config(page_title="Rtv.ai Pro v1", page_icon="🔧", layout="centered")

LANGS = {
    "Français": {
        "brand_sub": "Pro",
        "marque": "Marque",
        "modele": "Modèle & Motorisation",
        "modele_ph": "ex: W212 E350 V6",
        "probleme": "Symptôme ou code erreur",
        "probleme_ph": "ex: bruit injecteur ou P0299",
        "btn": "LANCER LE DIAGNOSTIC RAPIDE",
        "spinner": "Analyse en cours...",
        "err_key": "❌ Clé API manquante dans les secrets.",
        "err_gen": "Erreur : ",
        "warn": "⚠️ Remplis tous les champs.",
        "res": "Résultat",
        "history": "📜 Historique des diagnostics",
        "copy_label": "📋 Texte brut pour copie rapide :",
        "rate_title": "⭐ Noter l'application",
        "pseudo_ph": "Ton pseudo (ex: Meca91)",
        "comment_ph": "Ton avis...",
        "rate_btn": "Envoyer",
        "rate_thanks": "🙏 Merci pour ton retour !",
        "already_voted": "✅ Tu as déjà posté un avis !",
        "lang_label": "🌍 Langue",
    }
}
# J'ai réduit le dico de langues pour l'exemple mais tu peux recoller toutes tes langues ici.
# J'utilise juste le Français pour que tu testes le design sans avoir 300 lignes de dico.

REVIEWS_FILE = "avis.json"

def charger_avis():
  if os.path.exists(REVIEWS_FILE):
    try:
      with open(REVIEWS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    except:
      return []
  return []

def sauvegarder_avis(liste_avis):
  with open(REVIEWS_FILE, "w", encoding="utf-8") as f:
    json.dump(liste_avis, f, ensure_ascii=False, indent=4)

# --- CSS FORCE BRUTE ---
st.markdown(
    """
    <style>
    /* Le fond avec ta Mercedes reste intouchable */
    .stApp {
        background: 
            linear-gradient(rgba(7, 9, 19, 0.88), rgba(19, 24, 41, 0.92)),
            url("https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=1200&q=80");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    /* Force TOUT le texte en blanc par défaut */
    h1, h2, h3, p, label, div {
        color: #ffffff !important;
    }

    /* Le "Pro" du titre en rouge */
    .titre-pro {
        color: #ff2a2a !important;
        text-shadow: 0 0 10px rgba(255, 42, 42, 0.5);
    }

    /* === BOUTONS ULTRA AGRESSIFS === */
    [data-testid="baseButton-secondary"], div.stButton > button {
        background: linear-gradient(90deg, #ff0000 0%, #990000 100%) !important;
        color: white !important;
        border: 2px solid #ff4d4d !important;
        border-radius: 12px !important;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.5) !important;
        font-size: 18px !important;
        font-weight: 900 !important;
        letter-spacing: 1px !important;
        padding: 1rem !important;
        width: 100% !important;
        transition: 0.3s all ease !important;
        text-transform: uppercase !important;
    }
    [data-testid="baseButton-secondary"]:hover, div.stButton > button:hover {
        background: linear-gradient(90deg, #ff3333 0%, #cc0000 100%) !important;
        box-shadow: 0 0 35px rgba(255, 0, 0, 0.8) !important;
        transform: scale(1.02) !important;
        border-color: #ffffff !important;
    }

    /* === CHAMPS DE TEXTE VERRE FUMÉ === */
    [data-baseweb="input"], [data-baseweb="select"], [data-baseweb="textarea"] {
        background-color: rgba(0, 0, 0, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
    }
    [data-baseweb="input"]:focus-within, [data-baseweb="textarea"]:focus-within {
        border-color: #ff2a2a !important;
        box-shadow: 0 0 15px rgba(255, 42, 42, 0.4) !important;
    }
    
    /* Textes à l'intérieur des inputs */
    input, textarea, div[class*="stSelectbox"] span {
        color: #ffffff !important;
        font-size: 16px !important;
        font-weight: bold !important;
    }

    /* === BOÎTES D'HISTORIQUE ET RÉSULTATS === */
    [data-testid="stExpander"] {
        background-color: rgba(15, 20, 30, 0.8) !important;
        border: 1px solid #ff2a2a !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
    }
    [data-testid="stExpander"] summary {
        color: #ff2a2a !important;
        font-weight: bold !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Titre
st.markdown(
    "# 🔧 Rtv.ai <span class='titre-pro'>Pro</span>", unsafe_allow_html=True
)

api_key = None
if "GEMINI_API_KEY" in st.secrets:
  api_key = st.secrets["GEMINI_API_KEY"]
elif "GEMINI_API_KEY" in os.environ:
  api_key = os.environ["GEMINI_API_KEY"]

if api_key:
  genai.configure(api_key=api_key)

if "langue_choisie" not in st.session_state:
  st.session_state["langue_choisie"] = "Français"

if "historique" not in st.session_state:
  st.session_state["historique"] = []

if "a_deja_vote" not in st.session_state:
  st.session_state["a_deja_vote"] = False

# J'ai forcé sur Français pour ce test de design. Remets ton dico LANGS si besoin.
t = LANGS["Français"] 

col1, col2 = st.columns(2)
with col1:
  marque_choisie = st.selectbox(
      t["marque"],
      ["Mercedes-Benz", "BMW", "Audi", "Volkswagen", "Renault", "Peugeot"],
  )
with col2:
  modele = st.text_input(t["modele"], placeholder=t["modele_ph"])

probleme = st.text_input(t["probleme"], placeholder=t["probleme_ph"])

if st.button(t["btn"]):
  if not api_key:
    st.error(t["err_key"])
  elif modele and probleme:
    try:
      with st.spinner(t["spinner"]):
        model = genai.GenerativeModel("gemini-3.6-flash")

        prompt = f"""
        Expert mécanicien. Véhicule: {marque_choisie} {modele}. Symptôme ou code erreur: "{probleme}".
        RÈGLE ABSOLUE : Réponds entièrement en Français.
        Donne une réponse ultra-courte, sans phrase de politesse, style mécano pressé.

        1. Coupable numéro 1 (La pièce précise en 1 ligne).
        2. Test rapide (Comment vérifier en 1 minute).
        3. Serrage / Référence (Si applicable).
        """

        response = model.generate_content(prompt)
        resultat_texte = response.text

        entree_historique = {
            "vehicule": f"{marque_choisie} {modele}",
            "symptome": probleme,
            "resultat": resultat_texte,
        }
        st.session_state["historique"].insert(0, entree_historique)

    except Exception as e:
      st.error(f"{t['err_gen']}{e}")
  else:
    st.warning(t["warn"])

if st.session_state["historique"]:
  dernier = st.session_state["historique"][0]
  st.markdown("---")
  st.markdown(f"### 📊 {t['res']} : {dernier['vehicule']} - {dernier['symptome']}")
  st.markdown(dernier["resultat"])
  st.code(dernier["resultat"], language="markdown")

if len(st.session_state["historique"]) > 0:
  with st.expander(t["history"]):
    for idx, item in enumerate(st.session_state["historique"]):
      st.markdown(f"**{item['vehicule']}** — *{item['symptome']}*")
      st.text(item["resultat"][:120] + "...")
      if idx < len(st.session_state["historique"]) - 1:
        st.divider()
