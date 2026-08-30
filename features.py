import json
import streamlit as st
import requests

# --- CONFIGURATION AUTHENTIFICATION ---
# Tu peux récupérer tes identifiants sur la console Firebase (Firebase Auth / Web API Key)
FIREBASE_WEB_API_KEY = st.secrets.get("AIzaSyCSzQw2K1Vx7LWgzu63PXjLaG5toNov1fo", "")


def inscription_email(email, password):
    """Crée un compte utilisateur via Email/Mot de passe."""
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_WEB_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}

    res = requests.post(url, json=payload)
    data = res.json()

    if "error" in data:
        return False, data["error"]["message"]
    return True, data


def connexion_email(email, password):
    """Connecte un utilisateur via Email/Mot de passe."""
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}

    res = requests.post(url, json=payload)
    data = res.json()

    if "error" in data:
        return False, data["error"]["message"]
    return True, data


def afficher_interface_auth(translations):
    """Affiche le formulaire de connexion / inscription propre dans la page."""
    t = translations

    if "user" not in st.session_state:
        st.session_state.user = None

    # Si déjà connecté, afficher le profil
    if st.session_state.user:
        st.sidebar.success(f"👤 {st.session_state.user['email']}")
        if st.sidebar.button("Déconnexion", key="btn_logout"):
            st.session_state.user = None
            st.rerun()
        return True

    # Sinon, afficher l'interface de connexion / inscription
    st.sidebar.markdown("### 🔐 Espace Compte")
    tab_login, tab_signup = st.sidebar.tabs(["Connexion", "Inscription"])

    with tab_login:
        email = st.text_input(
            "Email", key="login_email", placeholder="meca@exemple.com"
        )
        pwd = st.text_input("Mot de passe", type="password", key="login_pwd")

        if st.button("Se connecter", key="btn_login_submit"):
            if email and pwd:
                success, result = connexion_email(email, pwd)
                if success:
                    st.session_state.user = {"email": email, "token": result["idToken"]}
                    st.success("Connexion réussie !")
                    st.rerun()
                else:
                    st.error(f"Erreur : {result}")
            else:
                st.warning("Remplis tous les champs.")

    with tab_signup:
        new_email = st.text_input(
            "Email", key="signup_email", placeholder="meca@exemple.com"
        )
        new_pwd = st.text_input("Mot de passe", type="password", key="signup_pwd")

        if st.button("Créer un compte", key="btn_signup_submit"):
            if new_email and new_pwd:
                if len(new_pwd) < 6:
                    st.warning("Le mot de passe doit faire au moins 6 caractères.")
                else:
                    success, result = inscription_email(new_email, new_pwd)
                    if success:
                        st.success("Compte créé ! Tu peux te connecter.")
                    else:
                        st.error(f"Erreur : {result}")
            else:
                st.warning("Remplis tous les champs.")

    return False
