import streamlit as st
import replicate
import os
import requests

# Astra Ayarları
st.set_page_config(page_title="Astra AI", page_icon="✨")
st.title("✨ Astra AI")

# Kullanıcıdan veri alma
komut = st.text_input("Astra'ya bir şeyler sor:")

if st.button("Gönder"):
    if komut:
        with st.spinner("Astra düşünüyor..."):
            try:
                # OpenRouter (Zeka Modu)
                headers = {"Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}"}
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json={"model": "meta-llama/llama-3-8b", "messages": [{"role": "user", "content": komut}]}
                )
                cevap = response.json()['choices'][0]['message']['content']
                st.write(cevap)
                
                # Eğer "resim" derse görsel oluştur
                if "resim yap" in komut.lower():
                    resim = replicate.run("black-forest-labs/flux-1.1-pro", input={"prompt": komut})
                    st.image(resim)
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
