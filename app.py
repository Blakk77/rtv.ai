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
