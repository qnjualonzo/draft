import streamlit as st
from transformers import pipeline
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline as summarizer_pipeline
import re

# Load the translation pipeline (English to French)
translation_pipeline = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")

# Load summarization pipeline
summarizer = summarizer_pipeline("summarization")

# Function to add spaces between sentences
def add_spaces_between_sentences(text):
    text = re.sub(r'([.!?])(?=\S)', r'\1 ', text)
    return text

# Initialize session state variables
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
if "summarized_text" not in st.session_state:
    st.session_state.summarized_text = ""

if "lang_direction" not in st.session_state:
    st.session_state.lang_direction = "EN to FR"
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# Streamlit Title
st.title("Translation and Summarization")

# Language Direction
lang_direction = st.sidebar.radio("Select Translation Direction", ["EN to FR", "FR to EN"])

# Reset session state when language direction changes
if lang_direction != st.session_state.lang_direction:
    st.session_state.lang_direction = lang_direction
    st.session_state.input_text = ""
    st.session_state.translated_text = ""
    st.session_state.summarized_text = ""

# Input Text Area for entering text
st.session_state.input_text = st.text_area("Enter text to translate:", value=st.session_state.input_text)

# Translation button
if st.button("Translate"):
    if st.session_state.input_text.strip():
        # Set source and target languages based on user selection
        src_lang = "en" if st.session_state.lang_direction == "EN to FR" else "fr"
        tgt_lang = "fr" if st.session_state.lang_direction == "EN to FR" else "en"
        
        # Perform translation
        translated_result = translation_pipeline(st.session_state.input_text)
        st.session_state.translated_text = translated_result[0]['translation_text']
        st.session_state.translated_text = add_spaces_between_sentences(st.session_state.translated_text)
        st.session_state.summarized_text = ""

# Show Translated Text
if st.session_state.translated_text:
    st.text_area("Translated Text:", value=st.session_state.translated_text, height=150, disabled=True)

    # Summarize the translated text
    if st.button("Summarize"):
        if st.session_state.translated_text.strip():
            processed_text = add_spaces_between_sentences(st.session_state.translated_text)

            # Perform summarization
            summarized_result = summarizer(processed_text, max_length=150, min_length=50, do_sample=False)
            st.session_state.summarized_text = summarized_result[0]['summary_text']

# Show Summarized Text
if st.session_state.summarized_text:
    st.text_area("Summarized Text:", value=st.session_state.summarized_text, height=150, disabled=True)
