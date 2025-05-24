import streamlit as st
import requests

API_KEY = "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" 
MODEL = "openai/gpt-3.5-turbo"

def analyze_sentiment_gpt(text):
    messages = [
        {"role": "system", "content": "Kamu adalah asisten analisis sentimen yang hanya boleh membalas dengan kata 'Positif', 'Negatif', atau 'Netral', tanpa penjelasan tambahan."},
        {"role": "user", "content": f"Tolong analisis sentimen dari kalimat ini:\n{text}"}
    ]
    
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
    
    if response.status_code == 200:
        result = response.json()
        sentiment = result['choices'][0]['message']['content'].strip().capitalize()
        if sentiment not in ['Positif', 'Negatif', 'Netral']:
            sentiment = "Tidak dapat menentukan sentimen"
        return sentiment
    else:
        return f"Error: {response.status_code} - {response.text}"

st.title("Analisis Sentimen dengan GPT (OpenRouter API)")

user_input = st.text_area("Masukkan kalimat untuk analisis sentimen:")

if st.button("Analisis"):
    if user_input.strip() == "":
        st.warning("Mohon masukkan teks terlebih dahulu.")
    else:
        with st.spinner("Sedang menganalisis..."):
            hasil = analyze_sentiment_gpt(user_input)
            st.success(f"Hasil Sentimen: **{hasil}**")
