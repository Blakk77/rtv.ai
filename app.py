import os
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Rtv.ai Pro", page_icon="🔧", layout="centered")

LANGS = {
    "Français": {
        "brand_sub": "Pro",
        "marque": "Marque",
        "modele": "Modèle & Motorisation",
        "modele_ph": "ex: W212 E350 V6",
        "probleme": "Symptôme précis",
        "probleme_ph": "ex: bruit injecteur",
        "btn": "Lancer le diagnostic rapide",
        "spinner": "Analyse en cours...",
        "err_key": "❌ Clé API manquante dans les secrets.",
        "err_gen": "Erreur : ",
        "warn": "⚠️ Remplis tous les champs.",
        "res": "Résultat",
    },
    "English": {
        "brand_sub": "Pro",
        "marque": "Brand",
        "modele": "Model & Engine",
        "modele_ph": "e.g., W212 E350 V6",
        "probleme": "Specific Symptom",
        "probleme_ph": "e.g., injector noise",
        "btn": "Run Quick Diagnosis",
        "spinner": "Analyzing...",
        "err_key": "❌ API key missing in secrets.",
        "err_gen": "Error: ",
        "warn": "⚠️ Please fill in all fields.",
        "res": "Result",
    },
    "Русский": {
        "brand_sub": "Pro",
        "marque": "Марка",
        "modele": "Модель и двигатель",
        "modele_ph": "напр., W212 E350 V6",
        "probleme": "Симптом",
        "probleme_ph": "напр., шум форсунки",
        "btn": "Запустить диагностику",
        "spinner": "Анализ...",
        "err_key": "❌ Ключ API отсутствует.",
        "err_gen": "Ошибка: ",
        "warn": "⚠️ Заполните все поля.",
        "res": "Результат",
    },
    "Македонски": {
        "brand_sub": "Pro",
        "marque": "Марка",
        "modele": "Модел и мотор",
        "modele_ph": "пр: W212 E350 V6",
        "probleme": "Симптом",
        "probleme_ph": "пр: звук од бризгач",
        "btn": "Стартувај дијагностика",
        "spinner": "Анализа...",
        "err_key": "❌ Нема API клуч.",
        "err_gen": "Грешка: ",
        "warn": "⚠️ Пополнете ги сите полиња.",
        "res": "Резултат",
    },
    "Српски / Srpski": {
        "brand_sub": "Pro",
        "marque": "Marka",
        "modele": "Model i motorizacija",
        "modele_ph": "npr: W212 E350 V6",
        "probleme": "Simptom",
        "probleme_ph": "npr: zvuk dizne",
        "btn": "Pokreni dijagnostiku",
        "spinner": "Analiza u toku...",
        "err_key": "❌ Nedostaje API ključ.",
        "err_gen": "Greška: ",
        "warn": "⚠️ Popunite sva polja.",
        "res": "Rezultat",
    },
    "Hrvatski": {
        "brand_sub": "Pro",
        "marque": "Marka",
        "modele": "Model i motor",
        "modele_ph": "npr: W212 E350 V6",
        "probleme": "Simptom",
        "probleme_ph": "npr: zvuk injektora",
        "btn": "Pokreni dijagnostiku",
        "spinner": "Analiza u tijeku...",
        "err_key": "❌ Nedostaje API ključ.",
        "err_gen": "Greška: ",
        "warn": "⚠️ Ispunite sva polja.",
        "res": "Rezultat",
    },
    "Español": {
        "brand_sub": "Pro",
        "marque": "Marca",
        "modele": "Modelo y Motorización",
        "modele_ph": "ej: W212 E350 V6",
        "probleme": "Síntoma específico",
        "probleme_ph": "ej: ruido de inyector",
        "btn": "Iniciar diagnóstico rápido",
        "spinner": "Analizando...",
        "err_key": "❌ Falta la clave API en los secretos.",
        "err_gen": "Error: ",
        "warn": "⚠️ Rellena todos los campos.",
        "res": "Resultado",
    },
    "Deutsch": {
        "brand_sub": "Pro",
        "marque": "Marke",
        "modele": "Modell & Motorisierung",
        "modele_ph": "z.B. W212 E350 V6",
        "probleme": "Symptom",
        "probleme_ph": "z.B. Injektorengeräusch",
        "btn": "Schnelldiagnose starten",
        "spinner": "Analysiere...",
        "err_key": "❌ API-Schlüssel fehlt in den Secrets.",
        "err_gen": "Fehler: ",
        "warn": "⚠️ Bitte alle Felder ausfüllen.",
        "res": "Ergebnis",
    },
}

with st.sidebar:
  langue_cle = st.selectbox(
      "🌍 Langue / Language", list(LANGS.keys()), label_visibility="visible"
  )

t = LANGS[langue_cle]

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #070913 0%, #131829 50%, #070913 100%);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #090d19 0%, #0f1523 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Bouton avec des bords bien arrondis et un style propre */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #ff4b4b 0%, #e03131 100%);
        color: white;
        font-weight: bold;
        border-radius: 16px;
        padding: 0.7rem;
        border: none;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        background: linear-gradient(135deg, #ff2b2b 0%, #c92a2a 100%);
        box-shadow: 0 6px 20px rgba(255, 43, 43, 0.6);
        transform: translateY(-1px);
    }

    /* Champs de saisie ultra arrondis pour dire adieu au look carré */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: rgba(255, 255, 255, 0.04);
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f"# 🔧 Rtv.ai <span style='color:#ff4b4b;'>{t['brand_sub']}</span>",
    unsafe_allow_html=True,
)

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
        Expert mécanicien. Véhicule: {marque_choisie} {modele}. Symptôme: "{probleme}".
        RÈGLE ABSOLUE : Réponds entièrement en {langue_cle}.
        Donne une réponse ultra-courte, sans phrase de politesse, style mécano pressé.

        1. Coupable numéro 1 (La pièce précise en 1 ligne).
        2. Test rapide (Comment vérifier en 1 minute).
        3. Serrage / Référence (Si applicable).
        """

        response = model.generate_content(prompt)

        st.markdown("---")
        st.markdown(
            f"### 📊 {t['res']} : {marque_choisie} ({modele}) - {probleme}"
        )
        st.markdown(response.text)

    except Exception as e:
      st.error(f"{t['err_gen']}{e}")
  else:
    st.warning(t["warn"])
