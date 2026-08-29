
st.markdown(
    """
    <style>
    .stApp {
        background: 
            linear-gradient(rgba(7, 9, 19, 0.88), rgba(19, 24, 41, 0.92)),
            url("https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=1200&q=80");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    /* Force le texte en blanc sauf les spans colorés spécifiquement */
    .stApp, div[data-testid="stMarkdownContainer"] p, div[data-testid="stMarkdownContainer"] li, label {
        color: #ffffff !important;
    }

    div.stButton > button {
        width: 100% !important;
        display: block !important;
        background: linear-gradient(135deg, #ff4b4b 0%, #e03131 100%);
        color: white;
        font-weight: bold;
        border-radius: 16px;
        padding: 0.7rem;
        border: none;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4);
        transition: all 0.3s ease;
        margin: 0 auto;
    }
    div.stButton > button:hover { 
        background: linear-gradient(135deg, #ff2b2b 0%, #c92a2a 100%);
        box-shadow: 0 6px 20px rgba(255, 43, 43, 0.6);
        transform: translateY(-1px);
    }

    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
        background-color: rgba(15, 23, 42, 0.6);
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: white;
    }
    </style>
""",
    unsafe_allow_html=True,
)
