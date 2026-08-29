import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Rtv.ai - Atelier Pro", page_icon="🔧", layout="centered"
)

# Design CSS custom pour un look plus moderne et pro (type dashboard atelier)
st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ff2b2b;
        color: white;
    }
    .card-box {
        background-color: #161a22;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #30363d;
        margin-bottom: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# En-tête stylé
st.markdown("# 🔧 Rtv.ai <span style='color:#ff4b4b;'>Pro Diagnostic</span>", unsafe_allow_html=True)
st.markdown(
    "<p style='color: #8b949e;'>Base de données technique constructeur"
    " instantanée.</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Formulaire principal en colonnes / blocs propres
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
    "Description du problème",
    placeholder=(
        "ex: Bruit suspect côté passager, perte de puissance à l'accélération..."
    ),
    height=100,
)

st.markdown("<br>", unsafe_allow_html=True)

# Base de données technique embarquée (Ultra rapide)
db_technique = {
    "Mercedes-Benz": {
        "specs_generales": (
            "Capacité huile V6 : 7.0L - 8.0L (Norme MB 229.51/52). Couples"
            " serrage roues : 150 Nm."
        ),
        "pannes_frequentes": [
            "Bruit / Couinement côté droit : Usure de la poulie de renvoi de courroie d'accessoires ou galet tendeur.",
            (
                "Claquement à froid : Poussoirs hydrauliques ou tendeur de chaîne"
                " de distribution fatigué."
            ),
            (
                "Perte de puissance : Durite de suralimentation (intercooler)"
                " micro-fissurée."
            ),
        ],
        "procedure_diag": (
            "1. Déposer le cache moteur supérieur.\n2. Inspecter l'alignement"
            " de la courroie accessoires moteur tournant.\n3. Utiliser un"
            " stéthoscope pour localiser le bruit sur les galets.\n4. Contrôler"
            " visuellement les durites de suralimentation."
        ),
    },
    "BMW": {
        "specs_generales": (
            "Capacité huile L6 : 6.5L (5W30 / 0W40). Couples serrage roues :"
            " 120 Nm."
        ),
        "pannes_frequentes": [
            "Bruit métallique arrière moteur : Chaîne de distribution détendue (patins usés).",
            "Surchauffe intermittente : Thermostat piloté ou pompe à eau électrique.",
        ],
        "procedure_diag": (
            "1. Interrogation des codes défauts OBD2.\n2. Contrôle du circuit"
            " de refroidissement.\n3. Vérification de l'état de la"
            " distribution."
        ),
    },
}

if st.button("Lancer l'analyse Autodata"):
  if modele_motorisation and probleme:
    st.markdown("---")
    st.markdown(
        f"## 📊 Rapport Technique : {marque_choisie} ({modele_motorisation})"
    )

    # Récupération des données
    data = db_technique.get(
        marque_choisie,
        {
            "specs_generales": (
                "Consulter les données techniques constructeur spécifiques."
            ),
            "pannes_frequentes": [
                "Vérification des faisceaux électriques et capteurs.",
                "Contrôle de l'état des filtres et fluides.",
            ],
            "procedure_diag": (
                "1. Passage à la valise diagnostic OBD2.\n2. Contrôle visuel"
                " des éléments périphériques."
            ),
        },
    )

    # Affichage en blocs stylés
    st.markdown("#### ⚙️ Spécifications & Couples")
    st.info(data["specs_generales"])

    st.markdown("#### ⚠️ Pannes Connues (Database)")
    for p in data["pannes_frequentes"]:
      st.markdown(f"- {p}")

    st.markdown("#### 🛠️ Procédure de Diagnostic")
    st.code(data["procedure_diag"], language="markdown")

    st.success("✅ Analyse terminée avec succès (Génération instantanée).")
  else:
    st.warning("⚠️ Merci de remplir le modèle et de décrire le problème.")
