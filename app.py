import streamlit as st
from transformers import pipeline
import re

# Load Hugging Face models for translation and summarization
translation_pipeline = pipeline("translation", model="Helsinki-NLP/opus-mt-en-ko")  # English to Korean translation
summarization_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")  # Summarization model

if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
if "summarized_text" not in st.session_state:
    st.session_state.summarized_text = ""

def add_spaces_between_sentences(text):
    text = re.sub(r'([.!?])(?=\S)', r'\1 ', text)
    return text

def translate_text_huggingface(input_text, src_lang, tgt_lang):
    try:
        # For simplicity, this uses the translation model from English to Korean or vice versa
        if src_lang == "en" and tgt_lang == "ko":
            translated = translation_pipeline(input_text, max_length=512)
        elif src_lang == "ko" and tgt_lang == "en":
            translated = translation_pipeline(input_text, max_length=512)
        else:
            raise ValueError("Unsupported translation direction")
        return translated[0]['translation_text']
    except Exception as e:
        st.error(f"Error during translation: {e}")
        return ""

def summarize_with_huggingface(text, num_sentences=3):
    try:
        summary = summarization_pipeline(text, max_length=150, min_length=50, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        st.error(f"Error during summarization: {e}")
        return ""

st.title("EnKoreS")

if "lang_direction" not in st.session_state:
    st.session_state.lang_direction = "EN to KO"
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

lang_direction = st.sidebar.radio("Select Translation Direction", ["EN to KO", "KO to EN"])

if lang_direction != st.session_state.lang_direction:
    st.session_state.lang_direction = lang_direction
    st.session_state.input_text = ""
    st.session_state.translated_text = ""
    st.session_state.summarized_text = ""

st.session_state.input_text = st.text_area("Enter text to translate:", value=st.session_state.input_text)

if st.button("Translate"):
    if st.session_state.input_text.strip():
        src_lang = "en" if st.session_state.lang_direction == "EN to KO" else "ko"
        tgt_lang = "ko" if st.session_state.lang_direction == "EN to KO" else "en"
        st.session_state.translated_text = translate_text_huggingface(st.session_state.input_text, src_lang, tgt_lang)
        st.session_state.translated_text = add_spaces_between_sentences(st.session_state.translated_text)
        st.session_state.summarized_text = ""

if st.session_state.translated_text:
    st.text_area("Translated Text:", value=st.session_state.translated_text, height=150, disabled=True)

    if st.button("Summarize"):
        if st.session_state.translated_text.strip():
            processed_text = add_spaces_between_sentences(st.session_state.translated_text)
            st.session_state.summarized_text = summarize_with_huggingface(processed_text)

if st.session_state.summarized_text:
    st.text_area("Summarized Text:", value=st.session_state.summarized_text, height=150, disabled=True)
