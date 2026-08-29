import json
import os
import google.generativeai as genai
import streamlit as st

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
        "history": "📜 Historique des diagnostics",
        "copy_label": "📋 Texte brut pour copie rapide :",
        "rate_title": "⭐ Noter l'application et laisser un avis",
        "pseudo_ph": "Ton pseudo (ex: Meca91)",
        "comment_ph": "Ton avis sur l'application...",
        "rate_btn": "Envoyer mon avis",
        "rate_thanks": "🙏 Merci pour ton retour, ton avis a bien été enregistré !",
        "already_voted": "✅ Tu as déjà posté un avis avec ce pseudo !",
        "lang_label": "🌍 Choisir la langue",
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
        "history": "📜 Diagnosis History",
        "copy_label": "📋 Raw text for easy copying:",
        "rate_title": "⭐ Rate the app & leave a comment",
        "pseudo_ph": "Your pseudo (e.g., JohnDoe)",
        "comment_ph": "Your feedback about the app...",
        "rate_btn": "Submit Review",
        "rate_thanks": "🙏 Thanks for your feedback!",
        "already_voted": "✅ You have already posted a review!",
        "lang_label": "🌍 Choose Language",
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
        "history": "📜 История диагностик",
        "copy_label": "📋 Текст для быстрого копирования:",
        "rate_title": "⭐ Оценить приложение и оставить отзыв",
        "pseudo_ph": "Ваш псевдоним",
        "comment_ph": "Ваш отзыв...",
        "rate_btn": "Отправить отзыв",
        "rate_thanks": "🙏 Спасибо за отзыв!",
        "already_voted": "✅ Вы уже оставили отзыв!",
        "lang_label": "🌍 Выбрать язык",
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
        "history": "📜 Историја на дијагностика",
        "copy_label": "📋 Текст за брзо копирање:",
        "rate_title": "⭐ Оцени ја апликацијата и остави коментар",
        "pseudo_ph": "Твој псевдоним",
        "comment_ph": "Твој коментар...",
        "rate_btn": "Испрати коментар",
        "rate_thanks": "🙏 Благодарам!",
        "already_voted": "✅ Веќе имате оставено оценка!",
        "lang_label": "🌍 Избери јазик",
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
        "history": "📜 Istorija dijagnostike",
        "copy_label": "📋 Tekst za lako kopiranje:",
        "rate_title": "⭐ Oceni aplikaciju i ostavi komentar",
        "pseudo_ph": "Tvoj nadimak",
        "comment_ph": "Tvoj komentar...",
        "rate_btn": "Pošalji ocenu",
        "rate_thanks": "🙏 Hvala na povratnoj informaciji!",
        "already_voted": "✅ Već si poslao ocenu!",
        "lang_label": "🌍 Izaberi jezik",
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
        "history": "📜 Povijest dijagnostike",
        "copy_label": "📋 Tekst za jednostavno kopiranje:",
        "rate_title": "⭐ Ocijeni aplikaciju i ostavi komentar",
        "pseudo_ph": "Tvoj nadimak",
        "comment_ph": "Tvoj komentar...",
        "rate_btn": "Pošalji recenziju",
        "rate_thanks": "🙏 Hvala na recenziji!",
        "already_voted": "✅ Već si ostavio recenziju!",
        "lang_label": "🌍 Odaberi jezik",
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
        "history": "📜 Historial de diagnósticos",
        "copy_label": "📋 Texto para copia rápida:",
        "rate_title": "⭐ Califica la app y deja un comentario",
        "pseudo_ph": "Tu apodo",
        "comment_ph": "Tu comentario...",
        "rate_btn": "Enviar opinión",
        "rate_thanks": "🙏 ¡Gracias por tu comentario!",
        "already_voted": "✅ ¡Ya has enviado tu opinión!",
        "lang_label": "🌍 Elegir idioma",
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
        "history": "📜 Diagnoseverlauf",
        "copy_label": "📋 Text zum schnellen Kopieren:",
        "rate_title": "⭐ App bewerten & Kommentar hinterlassen",
        "pseudo_ph": "Dein Pseudonym",
        "comment_ph": "Dein Feedback...",
        "rate_btn": "Bewertung absenden",
        "rate_thanks": "🙏 Danke für dein Feedback!",
        "already_voted": "✅ Du hast bereits eine Bewertung abgegeben!",
        "lang_label": "🌍 Sprache wählen",
    },
}

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

# CSS global placé APRÈS les imports
st.markdown(
    """
    <style>
    .stApp {
        background: 
            linear-gradient(rgba(7, 9, 19, 0.88), rgba(19, 24, 41, 0.92)),
            url("https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=1200&q=80");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    /* Texte en blanc sauf le "Pro" en rouge */
    .stApp, div[data-testid="stMarkdownContainer"] p, div[data-testid="stMarkdownContainer"] li, label {
        color: #ffffff !important;
    }

    div.stButton > button {
        width: 100% !important;
        display: block !important;
        background: linear-gradient(135deg, #ff4b4b 0%, #e03131 100%);
        color: white;
        font-weight: bold;
        border-radius: 16px;
        padding: 0.7rem;
        border: none;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4);
        transition: all 0.3s ease;
        margin: 0 auto;
    }
    div.stButton > button:hover { 
        background: linear-gradient(135deg, #ff2b2b 0%, #c92a2a 100%);
        box-shadow: 0 6px 20px rgba(255, 43, 43, 0.6);
        transform: translateY(-1px);
    }

    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
        background-color: rgba(15, 23, 42, 0.6);
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: white;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Titre de l'app
st.markdown(
    "# 🔧 Rtv.ai <span style='color:#ff4b4b;'>Pro</span>", unsafe_allow_html=True
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

langue_cle = st.session_state["langue_choisie"]
t = LANGS[langue_cle]

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

# Affichage du dernier diagnostic en cours
if st.session_state["historique"]:
  dernier = st.session_state["historique"][0]
  st.markdown("---")
  st.markdown(f"### 📊 {t['res']} : {dernier['vehicule']} - {dernier['symptome']}")
  st.markdown(dernier["resultat"])

  st.markdown(f"<br><small>{t['copy_label']}</small>", unsafe_allow_html=True)
  st.code(dernier["resultat"], language="markdown")

# Historique dans un expander au milieu
if len(st.session_state["historique"]) > 0:
  with st.expander(t["history"]):
    for idx, item in enumerate(st.session_state["historique"]):
      st.markdown(f"**{item['vehicule']}** — *{item['symptome']}*")
      st.text(item["resultat"][:120] + "...")
      if idx < len(st.session_state["historique"]) - 1:
        st.divider()

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

# Sélecteur de langue en bas
nouvelle_langue = st.selectbox(
    LANGS[langue_cle]["lang_label"],
    list(LANGS.keys()),
    index=list(LANGS.keys()).index(langue_cle),
)
if nouvelle_langue != langue_cle:
  st.session_state["langue_choisie"] = nouvelle_langue
  st.rerun()

# --- BLOC AVIS & COMMENTAIRES ---
st.markdown("---")
st.markdown(f"### {t['rate_title']}")

if st.session_state["a_deja_vote"]:
  st.success(t["already_voted"])
else:
  etoiles = ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]

  col_r1, col_r2 = st.columns([1, 2])
  with col_r1:
    note_selectionnee = st.select_slider(
        "Note", options=etoiles, value="⭐⭐⭐⭐⭐", label_visibility="collapsed"
    )
  with col_r2:
    pseudo_input = st.text_input(
        "Pseudo", placeholder=t["pseudo_ph"], label_visibility="collapsed"
    )

  commentaire_input = st.text_area(
      "Avis", placeholder=t["comment_ph"], label_visibility="collapsed"
  )

  if st.button(t["rate_btn"]):
    if pseudo_input.strip() and commentaire_input.strip():
      avis_actuels = charger_avis()
      nouvel_avis = {
          "pseudo": pseudo_input.strip(),
          "note": note_selectionnee,
          "commentaire": commentaire_input.strip(),
      }
      avis_actuels.insert(0, nouvel_avis)
      sauvegarder_avis(avis_actuels)
      st.session_state["a_deja_vote"] = True
      st.success(t["rate_thanks"])
      st.rerun()
    else:
      st.warning("⚠️ Remplis ton pseudo et ton commentaire.")

# Affichage des avis enregistrés globalement
tous_les_avis = charger_avis()
if tous_les_avis:
  st.markdown("<br>", unsafe_allow_html=True)
  for rev in tous_les_avis:
    st.markdown(f"**{rev['pseudo']}** {rev['note']}")
    st.caption(f'"{rev["commentaire"]}"')
    st.divider()
