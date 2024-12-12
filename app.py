import streamlit as st
from transformers import pipeline
import re

# Load the translation pipeline (English to Spanish) and specify PyTorch framework
translation_pipeline = pipeline("translation", model="Helsinki-NLP/opus-mt-en-es", framework="pt")

# Function to add spaces between sentences
def add_spaces_between_sentences(text):
    text = re.sub(r'([.!?])(?=\S)', r'\1 ', text)
    return text

# Initialize session state variables
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

if "lang_direction" not in st.session_state:
    st.session_state.lang_direction = "EN to ES"
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# Custom title and styling
st.markdown(
    """
    <style>
        .title {
            font-size: 40px;
            font-weight: bold;
            color: #4CAF50;
            text-align: center;
            margin-bottom: 20px;
        }
        .subheader {
            font-size: 20px;
            color: #333;
            text-align: center;
        }
        .sidebar .sidebar-content {
            background-color: #f0f0f0;
            padding: 20px;
            border-radius: 8px;
        }
        .stTextArea>div>div>textarea {
            font-size: 16px;
            line-height: 1.6;
            padding: 10px;
            border-radius: 8px;
            border: 2px solid #ddd;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            padding: 10px 20px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
    </style>
    """, unsafe_allow_html=True
)

# Streamlit Title
st.markdown('<div class="title">Deep Learning Translation</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Translate text between English and Spanish using a transformer model</div>', unsafe_allow_html=True)

# Input Text Area for entering text
st.session_state.input_text = st.text_area("Enter text to translate:", value=st.session_state.input_text, height=200)

# Translation button
if st.button("Translate"):
    if st.session_state.input_text.strip():
        # Perform translation
        translated_result = translation_pipeline(st.session_state.input_text)
        st.session_state.translated_text = translated_result[0]['translation_text']
        st.session_state.translated_text = add_spaces_between_sentences(st.session_state.translated_text)

# Show Translated Text
if st.session_state.translated_text:
    st.text_area("Translated Text (Spanish):", value=st.session_state.translated_text, height=200, disabled=True)
