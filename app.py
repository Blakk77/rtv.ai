import json
import os
import time
import google.generativeai as genai
import streamlit as st
from google.api_core.exceptions import ResourceExhausted

from features import afficher_interface_auth

# 1. Configuration de la page (RÈGLE STREAMLIT : toujours en premier)
st.set_page_config(page_title="Rtv.ai Pro", page_icon="🔧", layout="centered")

# --- PARAMÈTRES ET SÉCURITÉ ---
DUREE_ATTENTE = 60  # 60 secondes de cooldown
PSEUDO_ADMIN = "Meca91"  # Ton pseudo pour ne JAMAIS attendre
REVIEWS_FILE = "avis.json"

# --- DICTIONNAIRE MULTILINGUE COMPLET ---
LANGS = {
    "English": {
        "title": "Rtv.ai Pro - AI Mechanic Assistant",
        "sub": "Diagnose mechanics and auto repairs in seconds.",
        "marque": "Brand",
        "modele": "Model & Engine",
        "modele_ph": "e.g.: W212 E350 V6",
        "probleme": "Symptom or error code",
        "probleme_ph": "e.g.: injector noise or P0299",
        "btn": "LAUNCH QUICK DIAGNOSIS",
        "spinner": "Analyzing...",
        "err_key": "❌ API Key missing in secrets.",
        "err_gen": "Error: ",
        "warn": "⚠️ Please fill in all fields.",
        "res": "Result",
        "history": "📜 Diagnosis History",
        "rate_title": "⭐ RATE THE APP & LEAVE A REVIEW",
        "pseudo_ph": "Your username (e.g.: Meca91)",
        "comment_ph": "Your review on the app...",
        "rate_btn": "Submit Review",
        "rate_thanks": "🙏 Thank you for your feedback!",
        "already_voted": "✅ You have already posted a review!",
        "wait_msg": "⏳ Server cooling down. Please wait **{time} sec** before the next diagnosis.",
        "ai_lang": "English"
    },
    "Français": {
        "title": "Rtv.ai Pro - Assistant Mécanique IA",
        "sub": "Diagnostiquez vos pannes mécaniques en quelques secondes.",
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
        "rate_title": "⭐ NOTER L'APPLICATION ET LAISSER UN AVIS",
        "pseudo_ph": "Ton pseudo (ex: Meca91)",
        "comment_ph": "Ton avis sur l'application...",
        "rate_btn": "Envoyer mon avis",
        "rate_thanks": "🙏 Merci pour ton retour !",
        "already_voted": "✅ Tu as déjà posté un avis !",
        "wait_msg": "⏳ Serveur en pause. Patiente **{time} sec** avant le prochain diag.",
        "ai_lang": "French"
    },
    "Deutsch": {
        "title": "Rtv.ai Pro - KI-Mechanik-Assistent",
        "sub": "Diagnostizieren Sie Fahrzeugprobleme in Sekundenschnelle.",
        "marque": "Marke",
        "modele": "Modell & Motorisierung",
        "modele_ph": "z.B.: W212 E350 V6",
        "probleme": "Symptom oder Fehlercode",
        "probleme_ph": "z.B.: Injektorgeräusch oder P0299",
        "btn": "SCHNALLDIAGNOSE STARTEN",
        "spinner": "Analyse läuft...",
        "err_key": "❌ API-Schlüssel fehlt in den Secrets.",
        "err_gen": "Fehler: ",
        "warn": "⚠️ Bitte füllen Sie alle Felder aus.",
        "res": "Ergebnis",
        "history": "📜 Diagnoseverlauf",
        "rate_title": "⭐ BEWERTEN SIE DIE APP & HINTERLASSEN SIE EINE BEWERTUNG",
        "pseudo_ph": "Ihr Benutzername (z.B.: Meca91)",
        "comment_ph": "Ihre Bewertung zur App...",
        "rate_btn": "Bewertung absenden",
        "rate_thanks": "🙏 Vielen Dank für Ihr Feedback!",
        "already_voted": "✅ Sie haben bereits eine Bewertung abgegeben!",
        "wait_msg": "⏳ Server macht Pause. Bitte warten Sie **{time} Sek.** vor der nächsten Diagnose.",
        "ai_lang": "German"
    },
    "Македонски": {
        "title": "Rtv.ai Pro - AI Механички асистент",
        "sub": "Дијагностицирајте ги дефектите на возилото за неколку секунди.",
        "marque": "Марка",
        "modele": "Модел и мотор",
        "modele_ph": "нпр: W212 E350 V6",
        "probleme": "Симптом или код за грешка",
        "probleme_ph": "нпр: звук на инјектор или P0299",
        "btn": "ЗАПОЧНИ БРЗА ДИЈАГНОСТИКА",
        "spinner": "Анализата е во тек...",
        "err_key": "❌ Недостасува API клуч во тајните.",
        "err_gen": "Грешка: ",
        "warn": "⚠️ Ве молиме пополнете ги сите полиња.",
        "res": "Резултат",
        "history": "📜 Историја на дијагностика",
        "rate_title": "⭐ ОЦЕНЕТЕ ЈА АПЛИКАЦИЈАТА И ОСТАВЕТЕ РЕЦЕНЗИЈА",
        "pseudo_ph": "Вашето корисничко име (нпр: Meca91)",
        "comment_ph": "Вашето мислење за апликацијата...",
        "rate_btn": "Испрати рецензија",
        "rate_thanks": "🙏 Ви благодариме за повратните информации!",
        "already_voted": "✅ Веќе објавивте рецензија!",
        "wait_msg": "⏳ Серверот е во пауза. Почекајте **{time} сек** пред следната дијагноза.",
        "ai_lang": "Macedonian"
    },
    "Српски": {
        "title": "Rtv.ai Pro - AI Механички асистент",
        "sub": "Дијагностикујте кварове на возилу у неколико секунди.",
        "marque": "Марка",
        "modele": "Модел и мотор",
        "modele_ph": "нпр: W212 E350 V6",
        "probleme": "Симптом или код грешке",
        "probleme_ph": "нпр: звук инјектора или P0299",
        "btn": "ПОКРЕНИ БРЗУ ДИЈАГНОСТИКУ",
        "spinner": "Анализа у току...",
        "err_key": "❌ Недостаје API кључ у тајнама.",
        "err_gen": "Грешка: ",
        "warn": "⚠️ Молимо попуните сва поља.",
        "res": "Резултат",
        "history": "📜 Историја дијагностике",
        "rate_title": "⭐ ОЦЕНИТЕ АПЛИКАЦИЈУ И ОСТАВИТЕ РЕЦЕНЗИЈУ",
        "pseudo_ph": "Ваше корисничко име (нпр: Meca91)",
        "comment_ph": "Ваше мишљење о апликацији...",
        "rate_btn": "Пошаљи рецензију",
        "rate_thanks": "🙏 Хвала вам на повратним информацијама!",
        "already_voted": "✅ Већ сте објавили рецензију!",
        "wait_msg": "⏳ Сервер је у паузи. Сачекајте **{time} сек** пре следеће дијагнозе.",
        "ai_lang": "Serbian"
    },
    "Hrvatski": {
        "title": "Rtv.ai Pro - AI Mehanički pomoćnik",
        "sub": "Dijagnosticirajte kvarove na vozilu u nekoliko sekundi.",
        "marque": "Marka",
        "modele": "Model i motor",
        "modele_ph": "npr: W212 E350 V6",
        "probleme": "Simptom ili kod pogreške",
        "probleme_ph": "npr: zvuk injektora ili P0299",
        "btn": "POKRENI BRZU DIJAGNOSTIKU",
        "spinner": "Analiza u tijeku...",
        "err_key": "❌ Nedostaje API ključ u tajnama.",
        "err_gen": "Pogreška: ",
        "warn": "⚠️ Molimo ispunite sva polja.",
        "res": "Rezultat",
        "history": "📜 Povijest dijagnostike",
        "rate_title": "⭐ OCIJENITE APLIKACIJU I OSTAVITE RECENZIJU",
        "pseudo_ph": "Vaše korisničko ime (npr: Meca91)",
        "comment_ph": "Vaša recenzija aplikacije...",
        "rate_btn": "Pošalji recenziju",
        "rate_thanks": "🙏 Hvala vam na povratnim informacijama!",
        "already_voted": "✅ Već ste objavili recenziju!",
        "wait_msg": "⏳ Poslužitelj je u pauzi. Pričekajte **{time} sek** prije sljedeće dijagnoze.",
        "ai_lang": "Croatian"
    },
    "Русский": {
        "title": "Rtv.ai Pro - ИИ Механический помощник",
        "sub": "Быстрая диагностика автомобильных неисправностей.",
        "marque": "Марка",
        "modele": "Модель и двигатель",
        "modele_ph": "напр: W212 E350 V6",
        "probleme": "Симптом или код ошибки",
        "probleme_ph": "напр: шум форсунки или P0299",
        "btn": "ЗАПУСТИТЬ БЫСТРУЮ ДИАГНОСТИКУ",
        "spinner": "Анализ...",
        "err_key": "❌ Отсутствует API ключ в секретах.",
        "err_gen": "Ошибка: ",
        "warn": "⚠️ Пожалуйста, заполните все поля.",
        "res": "Результат",
        "history": "📜 История диагностик",
        "rate_title": "⭐ ОЦЕНИТЕ ПРИЛОЖЕНИЕ И ОСТАВЬТЕ ОТЗЫВ",
        "pseudo_ph": "Ваше имя (напр: Meca91)",
        "comment_ph": "Ваш отзыв о приложении...",
        "rate_btn": "Отправить отзыв",
        "rate_thanks": "🙏 Спасибо за ваш отзыв!",
        "already_voted": "✅ Вы уже оставили отзыв!",
        "wait_msg": "⏳ Сервер отдыхает. Подождите **{time} сек** перед следующей диагностикой.",
        "ai_lang": "Russian"
    },
    "Türkçe": {
        "title": "Rtv.ai Pro - Yapay Zeka Mekanik Asistanı",
        "sub": "Araç arızalarını saniyeler içinde teşhis edin.",
        "marque": "Marka",
        "modele": "Model ve Motor",
        "modele_ph": "örn: W212 E350 V6",
        "probleme": "Belirti veya hata kodu",
        "probleme_ph": "örn: enjektör sesi veya P0299",
        "btn": "HIZLI TEŞHİSİ BAŞLAT",
        "spinner": "Analiz ediliyor...",
        "err_key": "❌ Gizli anahtarlarda API Anahtarı eksik.",
        "err_gen": "Hata: ",
        "warn": "⚠️ Lütfen tüm alanları doldurun.",
        "res": "Sonuç",
        "history": "📜 Teşhis Geçmişi",
        "rate_title": "⭐ UYGULAMAYI DEĞERLENDİRİN VE YORUM YAPIN",
        "pseudo_ph": "Kullanıcı adınız (örn: Meca91)",
        "comment_ph": "Uygulama hakkındaki yorumunuz...",
        "rate_btn": "Yorumu Gönder",
        "rate_thanks": "🙏 Geri bildiriminiz için teşekkürler!",
        "already_voted": "✅ Zaten bir yorum gönderdiniz!",
        "wait_msg": "⏳ Sunucu beklemede. Lütfen sonraki teşhisten önce **{time} sn** bekleyin.",
        "ai_lang": "Turkish"
    }
}

# --- MENU DÉROULANT SÉLECTION DE LANGUE ---
selected_lang = st.selectbox(
    "🌐 Language / Langue",
    ["English", "Français", "Deutsch", "Македонски", "Српски", "Hrvatski", "Русский", "Türkçe"],
    key="global_lang_selector"
)

# Chargement du dictionnaire actif
t = LANGS[selected_lang]

# Gestion de l'authentification dans la barre latérale ou en haut
est_connecte = afficher_interface_auth(t)

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

# --- CSS STYLISÉ ---
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

# --- EN-TÊTE PRINCIPAL ---
st.markdown(f"# 🔧 {t['title']}")
st.caption(t["sub"])

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

# Formulaire principal
col1, col2 = st.columns(2)
with col1:
    marque_choisie = st.selectbox(
        t["marque"],
        ["Mercedes-Benz", "BMW", "Audi", "Volkswagen", "Renault", "Peugeot"],
        key="select_brand"
    )
with col2:
    modele = st.text_input(t["modele"], placeholder=t["modele_ph"], key="input_modele")

probleme = st.text_input(t["probleme"], placeholder=t["probleme_ph"], key="input_probleme")

# --- GESTION DU MINUTEUR DE 60S ---
utilisateur_actuel = st.session_state.get("utilisateur", "")
est_admin = utilisateur_actuel == PSEUDO_ADMIN

temps_ecoule = time.time() - st.session_state["dernier_clic"]
temps_restant = int(DUREE_ATTENTE - temps_ecoule)

lancer_diag = False
if not est_admin and temps_restant > 0:
    st.warning(t["wait_msg"].format(time=temps_restant))
    st.button(t["btn"], disabled=True, key="btn_disabled")
else:
    if st.button(t["btn"], key="btn_lancer_diag"):
        st.session_state["dernier_clic"] = time.time()
        lancer_diag = True

# --- EXÉCUTION DIAGNOSTIC ---
if lancer_diag:
    if not api_key:
        st.error(t["err_key"])
    elif modele and probleme:
        try:
            with st.spinner(t["spinner"]):
                model = genai.GenerativeModel("gemini-3.6-flash")
                prompt = f"""
                You are an expert mechanic assistant.
                Vehicle: {marque_choisie} {modele}.
                Symptom/Issue: "{probleme}".
                
                Respond concisely and professionally in {t['ai_lang']}:
                1. Top Suspect / Faulty Part (precise)
                2. Quick 1-minute test
                3. Torque Specs / Part Reference (if applicable)
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
            key="slider_note"
        )
    with col_r2:
        pseudo_in = st.text_input("Pseudo", placeholder=t["pseudo_ph"], key="input_pseudo_avis")

    com_in = st.text_area("Avis", placeholder=t["comment_ph"], key="input_comment_avis")

    if st.button(t["rate_btn"], key="btn_submit_avis"):
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
    for a in tous_avis:
        st.markdown(f"**{a['pseudo']}** ({a['note']}) : {a['commentaire']}")
