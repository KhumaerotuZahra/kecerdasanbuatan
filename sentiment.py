import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "openai/gpt-3.5-turbo"

def analyze_sentiment_gpt(text):
    messages = [
        {"role": "system", "content": "Kamu adalah asisten analisis sentimen yang hanya boleh membalas dengan kata 'Positif', 'Negatif', atau 'Netral', tanpa penjelasan tambahan."},
        {"role": "user", "content": f"Tolong analisis sentimen dari kalimat ini:\n{text}"}
    ]
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": messages,
                "temperature": 0,
                "max_tokens": 10
            }
        )
        response.raise_for_status()
        result = response.json()
        sentiment = result['choices'][0]['message']['content'].strip().capitalize()
        if sentiment not in ['Positif', 'Negatif', 'Netral']:
            sentiment = "Tidak dapat menentukan sentimen"
        return sentiment
    except Exception as e:
        return f"Error: {e}"

st.title("Analisis Sentimen dengan GPT (OpenRouter API)")

user_input = st.text_area("Masukkan kalimat untuk analisis sentimen:")

if st.button("Analisis"):
    if user_input.strip() == "":
        st.warning("Mohon masukkan teks terlebih dahulu.")
    else:
        with st.spinner("Sedang menganalisis..."):
            hasil = analyze_sentiment_gpt(user_input)
            st.success(f"Hasil Sentimen: **{hasil}**")
