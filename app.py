import json
import os
import time
import google.generativeai as genai
import streamlit as st
from google.api_core.exceptions import ResourceExhausted

import streamlit as st

# Menu déroulant de choix de langue directement sur la page
selected_lang = st.selectbox(
    "🌐 Choose language / Choisir la langue",
    ["English", "Français", "Deutsch", "Македонски", "Српски", "Hrvatski", "Русский", "Türkçe"]
)

# Dictionnaire de traductions
translations = {
    "English": {
        "title": "Rtv.ai Pro - AI Mechanic Assistant",
        "sub": "Diagnose mechanics and auto repairs in seconds.",
        "input_label": "Describe your issue or enter an error code:",
        "placeholder": "Ex: Noise when braking, error code P0300...",
        "btn_analyze": "Analyze",
        "result_header": "Diagnosis & Solutions",
        "chat_placeholder": "Ask a follow-up question...",
    },
    "Français": {
        "title": "Rtv.ai Pro - Assistant Mécanique IA",
        "sub": "Diagnostiquez vos pannes mécaniques en quelques secondes.",
        "input_label": "Décrivez votre problème ou entrez un code défaut :",
        "placeholder": "Ex : Bruit au freinage, code P0300...",
        "btn_analyze": "Analyser",
        "result_header": "Diagnostic & Solutions",
        "chat_placeholder": "Posez une question complémentaire...",
    },
    "Deutsch": {
        "title": "Rtv.ai Pro - KI-Mechanik-Assistent",
        "sub": "Diagnostizieren Sie Fahrzeugprobleme in Sekundenschnelle.",
        "input_label": "Beschreiben Sie das Problem oder geben Sie einen Fehlercode ein:",
        "placeholder": "Z.B. Geräusche beim Bremsen, Fehlercode P0300...",
        "btn_analyze": "Analysieren",
        "result_header": "Diagnose & Lösungen",
        "chat_placeholder": "Stellen Sie eine weitere Frage...",
    },
    "Македонски": {
        "title": "Rtv.ai Pro - AI Механички асистент",
        "sub": "Дијагностицирајте ги дефектите на возилото за неколку секунди.",
        "input_label": "Опишете го проблемот или внесете код за грешка:",
        "placeholder": "Нпр: Врева при кочење, код P0300...",
        "btn_analyze": "Анализирај",
        "result_header": "Дијагноза и решенија",
        "chat_placeholder": "Постави дополнително прашање...",
    },
    "Српски": {
        "title": "Rtv.ai Pro - AI Механички асистент",
        "sub": "Дијагностикујте кварове на возилу у неколико секунди.",
        "input_label": "Опишите ваш проблем или унесите код грешке:",
        "placeholder": "Нпр: Бука при кочењу, код P0300...",
        "btn_analyze": "Анализирај",
        "result_header": "Дијагноза и решења",
        "chat_placeholder": "Поставите додатно питање...",
    },
    "Hrvatski": {
        "title": "Rtv.ai Pro - AI Mehanički pomoćnik",
        "sub": "Dijagnosticirajte kvarove na vozilu u nekoliko sekundi.",
        "input_label": "Opišite svoj problem ili unesite kod pogreške:",
        "placeholder": "Npr: Buka pri kočenju, kod P0300...",
        "btn_analyze": "Analiziraj",
        "result_header": "Dijagnoza i rješenja",
        "chat_placeholder": "Postavite dodatno pitanje...",
    },
    "Русский": {
        "title": "Rtv.ai Pro - ИИ Механический помощник",
        "sub": "Быстрая диагностика автомобильных неисправностей.",
        "input_label": "Опишите проблему или введите код ошибки:",
        "placeholder": "Напр: Шум при торможении, код P0300...",
        "btn_analyze": "Анализировать",
        "result_header": "Диагностика и решения",
        "chat_placeholder": "Задайте дополнительный вопрос...",
    },
    "Türkçe": {
        "title": "Rtv.ai Pro - Yapay Zeka Mekanik Asistanı",
        "sub": "Araç arızalarını saniyeler içinde teşhis edin.",
        "input_label": "Sorununuzu tanımlayın veya bir hata kodu girin:",
        "placeholder": "Örn: Fren yaparken ses, P0300 kodu...",
        "btn_analyze": "Analiz Et",
        "result_header": "Teşhis ve Çözümler",
        "chat_placeholder": "Ek bir soru sorun...",
    }
}

# Récupération de la traduction
t = translations[selected_lang]

# Affichage avec les textes traduits
st.title(t["title"])
st.caption(t["sub"])

user_input = st.text_input(t["input_label"], placeholder=t["placeholder"])
if st.button(t["btn_analyze"]):
    st.subheader(t["result_header"])

# Variable contenant les textes dans la langue sélectionnée
t = translations[st.session_state.lang]

# Affichage des éléments
st.title(t["title"])
st.caption(t["sub"])

if st.button(t["btn_analyze"], key="btn_analyze_submit"):
if st.button(t["btn_analyze"]):
    st.subheader(t["result_header"])
    # Ton code de traitement / API ici

# Exemple d'utilisation dans l'application
st.title(t["title"])

st.set_page_config(page_title="Rtv.ai Pro", page_icon="🔧", layout="centered")


# --- PARAMÈTRES ET SÉCURITÉ ---
DUREE_ATTENTE = 60  # 60 secondes de cooldown
PSEUDO_ADMIN = "Meca91"  # Ton pseudo pour ne JAMAIS attendre
REVIEWS_FILE = "avis.json"

LANGS = {
    "Français": {
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
        "rate_title": "⭐ NOTER L'APPLICATION ET LAISSER UN AVIS",
        "pseudo_ph": "Ton pseudo (ex: Meca91)",
        "comment_ph": "Ton avis sur l'application...",
        "rate_btn": "Envoyer mon avis",
        "rate_thanks": "🙏 Merci pour ton retour !",
        "already_voted": "✅ Tu as déjà posté un avis !",
    }
}

# --- FONCTIONS AVIS ---
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
    .stApp {
        background: linear-gradient(rgba(7, 9, 19, 0.88), rgba(19, 24, 41, 0.92)),
                    url("https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=1200&q=80");
        background-size: cover; background-attachment: fixed;
    }
    h1, h2, h3, p, label, div { color: #ffffff !important; }
    .titre-pro { color: #ff2a2a !important; text-shadow: 0 0 10px rgba(255, 42, 42, 0.5); }
    
    div.stButton > button {
        background: linear-gradient(90deg, #ff0000 0%, #990000 100%) !important;
        color: white !important; border: 2px solid #ff4d4d !important;
        border-radius: 12px !important; font-weight: 800 !important;
        padding: 0.8rem !important; width: 100% !important;
    }
    [data-baseweb="input"], [data-baseweb="select"], [data-baseweb="textarea"] {
        background-color: rgba(0, 0, 0, 0.75) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    "# 🔧 Rtv.ai <span class='titre-pro'>Pro</span>", unsafe_allow_html=True
)

# API Key
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
if api_key:
  genai.configure(api_key=api_key)

# Session States
if "historique" not in st.session_state:
  st.session_state["historique"] = []
if "dernier_clic" not in st.session_state:
  st.session_state["dernier_clic"] = 0
if "a_deja_vote" not in st.session_state:
  st.session_state["a_deja_vote"] = False

t = LANGS["Français"]

# Formulaire principal
col1, col2 = st.columns(2)
with col1:
  marque_choisie = st.selectbox(
      t["marque"],
      ["Mercedes-Benz", "BMW", "Audi", "Volkswagen", "Renault", "Peugeot"],
  )
with col2:
  modele = st.text_input(t["modele"], placeholder=t["modele_ph"])

probleme = st.text_input(t["probleme"], placeholder=t["probleme_ph"])

# --- GESTION DU MINUTEUR DE 60S ---
utilisateur_actuel = st.session_state.get("utilisateur", "")
est_admin = utilisateur_actuel == PSEUDO_ADMIN

temps_ecoule = time.time() - st.session_state["dernier_clic"]
temps_restant = int(DUREE_ATTENTE - temps_ecoule)

lancer_diag = False
if not est_admin and temps_restant > 0:
  st.warning(
      f"⏳ Serveur en pause. Patiente **{temps_restant} sec** avant le prochain"
      " diag."
  )
  st.button(t["btn"], disabled=True)
else:
  if st.button(t["btn"]):
    st.session_state["dernier_clic"] = time.time()
    lancer_diag = True

# --- EXÉCUTION DIAGNOSTIC ---
if lancer_diag:
  if not api_key:
    st.error(t["err_key"])
  elif modele and probleme:
    try:
      with st.spinner(t["spinner"]):
        # CORRECTION DU NOM DU MODÈLE (gemini-1.5-flash)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
        Expert mécanicien. Véhicule: {marque_choisie} {modele}. Symptôme: "{probleme}".
        Réponds court en Français style mécano:
        1. Coupable N°1 (pièce précise)
        2. Test rapide (1 min)
        3. Serrage / Réf
        """
        response = model.generate_content(prompt)
        st.session_state["historique"].insert(
            0,
            {
                "vehicule": f"{marque_choisie} {modele}",
                "symptome": probleme,
                "resultat": response.text,
            },
        )
    except ResourceExhausted:
      st.error("⏳ Quota dépassé ! Patiente 1 minute.")
    except Exception as e:
      st.error(f"{t['err_gen']}{e}")
  else:
    st.warning(t["warn"])

# Affichage des résultats & historique
if st.session_state["historique"]:
  dernier = st.session_state["historique"][0]
  st.markdown("---")
  st.markdown(f"### 📊 {t['res']} : {dernier['vehicule']}")
  st.markdown(dernier["resultat"])

if len(st.session_state["historique"]) > 1:
  with st.expander(t["history"]):
    for idx, item in enumerate(st.session_state["historique"][1:]):
      st.markdown(f"**{item['vehicule']}** — *{item['symptome']}*")
      st.caption(item["resultat"][:100] + "...")

# ==========================================
# --- SECTION AVIS (TOUT EN BAS DU CODE) ---
# ==========================================
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(f"### {t['rate_title']}")

if st.session_state["a_deja_vote"]:
  st.success(t["already_voted"])
else:
  col_r1, col_r2 = st.columns([1, 2])
  with col_r1:
    note_sel = st.select_slider(
        "Note",
        options=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
        value="⭐⭐⭐⭐⭐",
    )
  with col_r2:
    pseudo_in = st.text_input("Pseudo", placeholder=t["pseudo_ph"])

  com_in = st.text_area("Avis", placeholder=t["comment_ph"])

  if st.button(t["rate_btn"]):
    if pseudo_in.strip() and com_in.strip():
      avis_liste = charger_avis()
      avis_liste.insert(
          0,
          {
              "pseudo": pseudo_in.strip(),
              "note": note_sel,
              "commentaire": com_in.strip(),
          },
      )
      sauvegarder_avis(avis_liste)
      st.session_state["a_deja_vote"] = True
      st.success(t["rate_thanks"])
      st.rerun()
    else:
      st.warning("⚠️ Entre ton pseudo et ton avis avant d'envoyer.")

# Affichage des avis clients enregistrés
tous_avis = charger_avis()
if tous_avis:
  st.markdown("---")
  for av in tous_avis:
    st.markdown(f"**{av['pseudo']}** — {av['note']}")
    st.caption(f'"{av["commentaire"]}"')
