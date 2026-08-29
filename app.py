import streamlit as st

st.set_page_config(page_title="Rtv.ai", page_icon="🔧")

st.title("🔧 Rtv.ai - Base de Données Technique")
st.write(
    "Ton assistant mécanique intelligent couplé à une base technique constructeur."
)

# Étape 1 : Choix de la marque
marques = ["Mercedes-Benz", "BMW", "Audi", "Volkswagen", "Renault", "Peugeot"]
marque_choisie = st.selectbox("1. Choisis la marque du véhicule :", marques)

# Étape 2 : Saisie du modèle et du moteur
modele_motorisation = st.text_input(
    "2. Précise le modèle et la motorisation (ex: W212 E350 V6, Série 3 E90...)"
)

# Étape 3 : Description du problème
probleme = st.text_area("3. Décris le symptôme ou la panne :")

# Base de données Autodata simulée pour les specs / pannes courantes
database_autodata = {
    "Mercedes-Benz": {
        "specs": "Couples de serrage culasse : 20 Nm + 90°. Schéma courroie accessoires : Type standard avec galet tendeur automatique.",
        "pannes_frequentes": [
            "Usure prématurée des galets tendeurs (bruit de couinement)",
            "Fuite d'huile radiateur d'huile (Oil Cooler)",
            "Problème capteur PMH (démarrage difficile à chaud)",
        ],
    },
    "BMW": {
        "specs": "Capacité huile moteur 6 cylindres : 6.5L (5W30). Schéma courroie : Passer par le galet de renvoi en bas à droite.",
        "pannes_frequentes": [
            "Rupture chaîne de distribution (moteurs N47 / N20)",
            "Joints de queue de soupape durcis",
            "Surchauffe due au thermostat piloté",
        ],
    },
    "Audi": {
        "specs": "Couple serrage roues : 120 Nm. Pression turbo nominale : 1.4 bar (TDI / TFSI).",
        "pannes_frequentes": [
            "Vanne EGR encrassée",
            "Volant moteur bi-masse HS (bruit au point mort)",
            "Boîte S-Tronic : à-coups si vidange non faite à 60 000km",
        ],
    },
}

if st.button("Lancer la recherche Autodata & Diagnostic"):
  if modele_motorisation and probleme:
    with st.spinner("Recherche dans la base de données technique..."):
      st.success("Données trouvées !")

      # Affichage des infos techniques constructeur (Autodata)
      st.write(
          f"### 📚 Fiche Technique Constructeur ({marque_choisie} -"
          f" {modele_motorisation}) :"
      )

      if marque_choisie in database_autodata:
        data = database_autodata[marque_choisie]
        st.info(f"**Specs & Couples :** {data['specs']}")

        st.write("#### ⚠️ Pannes connues répertoriées (Database) :")
        for p in data["pannes_frequentes"]:
          st.write(f"- {p}")
      else:
        st.warning(
            "Données spécifiques génériques appliquées pour cette marque."
        )

      # Analyse ciblée du problème
      st.write("### 🔍 Diagnostic intelligent :")
      st.write(
          f"Analyse croisée pour ton problème : *'{probleme}'* sur ta"
          f" **{marque_choisie} {modele_motorisation}**."
      )
      st.warning(
          "💡 **Recommandation atelier :** Vérifie les éléments listés ci-dessus"
          " en priorité selon les notes techniques constructeur."
      )
  else:
    st.warning("Remplis bien le modèle et le problème stp.")
