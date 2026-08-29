import streamlit as st

st.set_page_config(
    page_title="Rtv.ai - Atelier Pro", page_icon="🔧", layout="centered"
)

st.markdown(
    """
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem;
        border: none;
    }
    .stButton>button:hover { background-color: #ff2b2b; color: white; }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    "# 🔧 Rtv.ai <span style='color:#ff4b4b;'>Pro Diagnostic</span>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='color: #8b949e;'>Base de données technique constructeur"
    " ciblée.</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown("### 📋 1. Identification du Véhicule")
marques = [
    "Mercedes-Benz",
    "BMW",
    "Audi",
    "Volkswagen",
    "Renault",
    "Peugeot",
    "Autre",
]
col1, col2 = st.columns(2)
with col1:
  marque_choisie = st.selectbox("Marque constructeur", marques)
with col2:
  modele_motorisation = st.text_input(
      "Modèle & Motorisation", placeholder="ex: W212 E350 V6"
  )

st.markdown("### 🔍 2. Symptôme / Panne constatée")
probleme = st.text_area(
    "Description précise du problème",
    placeholder=(
        "ex: perte de puissance à l'accélération, fumée noire, bruit de"
        " sifflement..."
    ),
    height=100,
)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Lancer l'analyse ciblée"):
  if modele_motorisation and probleme:
    st.markdown("---")
    st.markdown(
        f"## 📊 Rapport d'Analyse : {marque_choisie} ({modele_motorisation})"
    )
    st.write(f"🔎 **Symptôme analysé :** *{probleme}*")

    # Analyse intelligente basée sur les mots-clés saisis par l'utilisateur
    pb_lower = probleme.lower()

    if "puissance" in pb_lower or "pêche" in pb_lower or "accélération" in pb_lower:
      diagnostic_titre = "Problème de Puissance / Suralimentation"
      causes = [
          "Durite de suralimentation (intercooler) percée ou fendue (génère un sifflement et une mise en sécurité du turbo).",
          "Vanne EGR encrassée ou bloquée en position ouverte.",
          "Capteur de pression de suralimentation (MAP) encrassé par la suie.",
          "Filtre à carburant colmaté (débit insuffisant en charge).",
      ]
      actions = (
          "1. Inspecter minutieusement toutes les durites d'échangeur air/air"
          " (traces d'huile visibles).\n2. Contrôler les codes défauts à la"
          " valise (ex: pression de turbo trop basse).\n3. Nettoyer ou tester"
          " le capteur de pression MAP sur le collecteur."
      )

    elif "bruit" in pb_lower or "claque" in pb_lower or "couine" in pb_lower:
      diagnostic_titre = "Bruit / Anomalie Mécanique Périphérique"
      causes = [
          "Usure du galet tendeur ou de la poulie de renvoi de la courroie d'accessoires.",
          "Jeu au niveau de la poulie debrayable d'alternateur.",
          "Jeu ou usure des poussoirs hydrauliques / chaîne de distribution.",
      ]
      actions = (
          "1. Déposer la courroie d'accessoires et vérifier l'état de chaque"
          " galet à la main.\n2. Écouter le bloc moteur avec un stéthoscope"
          " d'atelier.\n3. Vérifier la tension de la chaîne."
      )

    else:
      diagnostic_titre = "Diagnostic Général / Panne Spécifique"
      causes = [
          "Anomalie de gestion électronique ou capteur défectueux.",
          "Faux contact sur les faisceaux moteurs ou problème d'alimentation.",
      ]
      actions = (
          "1. Brancher un outil de diagnostic OBD2 pour relever les codes"
          " défauts précis.\n2. Contrôler l'état des fusibles et des masses"
          " principales."
      )

    # Affichage dynamique orienté vers le vrai problème
    st.markdown(f"#### ⚙️ Cause Principale Identifiée : {diagnostic_titre}")
    st.markdown("#### ⚠️ Pannes Probables à Vérifier :")
    for c in causes:
      st.markdown(f"- {c}")

    st.markdown("#### 🛠️ Procédure de Résolution Recommandée :")
    st.code(actions, language="markdown")

    st.success("✅ Analyse effectuée en fonction de votre description.")
  else:
    st.warning("⚠️ Merci de remplir le modèle et de décrire le problème.")
