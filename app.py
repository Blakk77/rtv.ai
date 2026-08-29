import streamlit as st

st.set_page_config(page_title="Rtv.ai", page_icon="🔧")

st.title("🔧 Rtv.ai")
st.write("Ton assistant mécanique intelligent.")

probleme = st.text_area("Décris le problème de la voiture :")

if st.button("Lancer l'analyse"):
    if probleme:
        st.success("Analyse en cours...")
        # Ici on ajoutera le cerveau de l'IA juste après !
    else:
        st.warning("Écris d'abord un problème stp.")
