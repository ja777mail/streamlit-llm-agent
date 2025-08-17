import os
import streamlit as st
from openai import OpenAI

# Код (универсальный, работает и локально, и в Streamlit Cloud):
# Берём API-ключ: сначала из переменной окружения, потом из st.secrets

# Читаем API ключ
api_key = os.environ.get("OPENAI_API_KEY") or st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

st.title("💬 Мини LLM агент на Streamlit")

# Поле для ввода
prompt = st.text_input("Введите запрос:")

# Кнопка
if st.button("Отправить"):
    if prompt.strip():
        with st.spinner("Генерация ответа..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
            )
            # ✅ Исправлено: используем .content вместо индекса
            st.write("**Ответ:**", response.choices[0].message.content)
    else:
        st.warning("Введите текст перед отправкой!")
