import json
import os
import time
import google.generativeai as genai
import streamlit as st
from google.api_core.exceptions import ResourceExhausted

st.set_page_config(page_title="Rtv.ai Pro", page_icon="🔧", layout="centered")

# --- 1. CONFIG & CONSTANTES ---
DUREE_ATTENTE = 60
PSEUDO_ADMIN = "adminmkd"
REVIEWS_FILE = "avis.json"

# Récupération de la clé API Gemini
api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")
if api_key:
    genai.configure(api_key=api_key)

# Dictionnaire de langue
LANGS = {
    "Français": {
        "marque": "Marque du véhicule",
        "modele": "Modèle",
        "modele_ph": "ex: Golf 7 2.0 TDI",
        "probleme": "Symptôme / Code erreur",
        "probleme_ph": "ex: Perte de puissance + voyant moteur",
        "btn": "🚀 Lancer le diagnostic pro",
        "spinner": "Analyse du problème par l'IA...",
        "err_key": "Clé API Gemini introuvable.",
        "err_gen": "Erreur : ",
        "warn": "Remplis tous les champs.",
        "res": "Résultat",
        "history": "📜 Historique des diags récents",
        "rate_title": "💬 Laisser un avis",
        "already_voted": "Merci ! Ton avis a déjà été enregistré.",
        "pseudo_ph": "Ton pseudo...",
        "comment_ph": "Ton retour d'expérience...",
        "rate_btn": "Envoyer l'avis",
        "rate_thanks": "Avis envoyé avec succès !",
    }
}
t = LANGS["Français"]

# --- 2. FONCTIONS UTILES (AVIS) ---
def charger_avis():
    if os.path.exists(REVIEWS_FILE):
        try:
            with open(REVIEWS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def sauvegarder_avis(liste_avis):
    with open(REVIEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(liste_avis, f, ensure_ascii=False, indent=2)

# --- 3. SESSION STATES ---
if "historique" not in st.session_state:
    st.session_state["historique"] = []
if "dernier_clic" not in st.session_state:
    st.session_state["dernier_clic"] = 0
if "a_deja_vote" not in st.session_state:
    st.session_state["a_deja_vote"] = False

# --- 4. VERIF ADMIN (SIDEBAR) ---
with st.sidebar:
    pass_input = st.text_input("Accès Admin", type="password", placeholder="Mot de passe...")

est_admin = pass_input.strip().lower() == PSEUDO_ADMIN or st.query_params.get("admin", "").lower() == PSEUDO_ADMIN

if est_admin:
    st.session_state["dernier_clic"] = 0

# --- 5. BANDEAU ADMIN EN HAUT ---
if est_admin:
    st.markdown("""
        <div style="background-color: rgba(255, 42, 42, 0.15); border: 1px solid #ff2a2a; color: #ff4d4d; padding: 8px 15px; border-radius: 8px; text-align: center; font-weight: bold; margin-bottom: 20px;">
            ⚡ Compte Admin connecté — Cooldown désactivé
        </div>
    """, unsafe_allow_html=True)

st.markdown("# 🔧 Rtv.ai Pro")

# --- 6. FORMULAIRE PRINCIPAL ---
col1, col2 = st.columns(2)
with col1:
    marque_choisie = st.selectbox(
        t["marque"],
        ["Mercedes-Benz", "BMW", "Audi", "Volkswagen", "Renault", "Peugeot"],
    )
with col2:
    modele = st.text_input(t["modele"], placeholder=t["modele_ph"])

probleme = st.text_input(t["probleme"], placeholder=t["probleme_ph"])

# --- 7. MINUTEUR ET BOUTON ---
temps_ecoule = time.time() - st.session_state["dernier_clic"]
temps_restant = int(DUREE_ATTENTE - temps_ecoule)

lancer_diag = False
if not est_admin and temps_restant > 0:
    st.warning(f"⏳ Serveur en pause. Patiente **{temps_restant} sec** avant le prochain diag.")
    st.button(t["btn"], disabled=True)
else:
    if st.button(t["btn"]):
        st.session_state["dernier_clic"] = time.time()
        lancer_diag = True

# --- 8. EXECUTION DIAGNOSTIC ---
if lancer_diag:
    if not api_key:
        st.error(t["err_key"])
    elif modele and probleme:
        try:
            with st.spinner(t["spinner"]):
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

# --- 9. RESULTATS & HISTORIQUE ---
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

# --- 10. SECTION AVIS ---
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
