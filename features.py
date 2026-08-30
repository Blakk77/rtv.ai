import time
import extra_streamlit_components as stx
import requests
import streamlit as st

# Clé API Firebase
FIREBASE_WEB_API_KEY = (
    st.secrets.get("FIREBASE_WEB_API_KEY")
    or "AIzaSyCSzQw2K1Vx7LWgzu63PXjLaG5toNov1fo"
)


def get_cookie_manager():
    return stx.CookieManager()


def connexion_email(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    res = requests.post(url, json=payload)
    return res.json()


def inscription_email(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_WEB_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    res = requests.post(url, json=payload)
    return res.json()


def valider_token_firebase(id_token):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={FIREBASE_WEB_API_KEY}"
    payload = {"idToken": id_token}
    res = requests.post(url, json=payload)
    data = res.json()
    if "users" in data:
        return True, data["users"][0]["email"]
    return False, None


def afficher_interface_auth(t):
    cookie_manager = get_cookie_manager()

    # Récupération du cookie existant
    auth_token = cookie_manager.get(cookie="rtv_auth_token")

    if "utilisateur" not in st.session_state:
        st.session_state.utilisateur = None

    if st.session_state.utilisateur is None and auth_token:
        valide, email = valider_token_firebase(auth_token)
        if valide:
            st.session_state.utilisateur = email

    # Utilisateur connecté
    if st.session_state.utilisateur:
        st.sidebar.success(f"👤 {st.session_state.utilisateur}")
        if st.sidebar.button("Déconnexion", key="btn_logout"):
            cookie_manager.delete("rtv_auth_token")
            st.session_state.utilisateur = None
            time.sleep(0.5)
            st.rerun()
        return True

    # Formulaire de connexion / inscription
    st.sidebar.markdown("### 🔐 Espace Compte")
    tab_connexion, tab_inscription = st.sidebar.tabs(
        ["Connexion", "Inscription"]
    )

    with tab_connexion:
        email = st.text_input("Email", key="login_email")
        pwd = st.text_input("Mot de passe", type="password", key="login_pwd")
        if st.button("Se connecter", key="btn_login"):
            if email and pwd:
                res = connexion_email(email, pwd)
                if "idToken" in res:
                    token = res["idToken"]
                    cookie_manager.set("rtv_auth_token", token, max_age=2592000)
                    st.session_state.utilisateur = email
                    st.success("Connexion réussie !")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    err = res.get("error", {}).get("message", "Erreur inconnue")
                    st.error(f"Erreur : {err}")
            else:
                st.warning("Remplis tous les champs.")

    with tab_inscription:
        email_reg = st.text_input("Email", key="reg_email")
        pwd_reg = st.text_input(
            "Mot de passe", type="password", key="reg_pwd"
        )
        if st.button("Créer un compte", key="btn_reg"):
            if email_reg and pwd_reg:
                res = inscription_email(email_reg, pwd_reg)
                if "idToken" in res:
                    token = res["idToken"]
                    cookie_manager.set("rtv_auth_token", token, max_age=2592000)
                    st.session_state.utilisateur = email_reg
                    st.success("Compte créé avec succès !")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    err = res.get("error", {}).get("message", "Erreur inconnue")
                    st.error(f"Erreur : {err}")
            else:
                st.warning("Remplis tous les champs.")

    return False
