import json
import os
import time
import google.generativeai as genai
import streamlit as st
from google.api_core.exceptions import ResourceExhausted

st.set_page_config(page_title="Rtv.ai Pro", page_icon="🔧", layout="centered")

# --- CONFIG & SESSION ---
DUREE_ATTENTE = 60
PSEUDO_ADMIN = "adminmkd"

if "historique" not in st.session_state:
    st.session_state["historique"] = []
if "dernier_clic" not in st.session_state:
    st.session_state["dernier_clic"] = 0

# --- VERIF ADMIN SIDEBAR ---
with st.sidebar:
    pass_input = st.text_input("Accès Admin", type="password", placeholder="Mot de passe...")

# On définit est_admin UNE SEULE FOIS ici tout en haut
est_admin = pass_input.strip().lower() == PSEUDO_ADMIN or st.query_params.get("admin", "").lower() == PSEUDO_ADMIN

if est_admin:
    st.session_state["dernier_clic"] = 0

# --- BANDEAU ADMIN (EN HAUT DE PAGE) ---
if est_admin:
    st.markdown("""
        <div style="background-color: rgba(255, 42, 42, 0.15); border: 1px solid #ff2a2a; color: #ff4d4d; padding: 8px 15px; border-radius: 8px; text-align: center; font-weight: bold; margin-bottom: 20px;">
            ⚡ Compte Admin connecté — Cooldown désactivé
        </div>
    """, unsafe_allow_html=True)

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
        model = genai.GenerativeModel("gemini-3.6-flash")
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
