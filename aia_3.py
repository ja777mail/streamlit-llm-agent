import os
import streamlit as st
from openai import OpenAI

# Инициализация клиента
# client = OpenAI()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
# model = "gpt-5-nano"
st.set_page_config(page_title="LLM Агент", page_icon="🤖")
st.title("🤖 LLM Агент со стримингом")

# Ввод пользователя
user_input = st.text_area(
    "Введите запрос:", "Напиши короткий рассказ о роботе, который научился чувствовать."
)

if st.button("Запустить"):
    st.write("### Ответ:")
    # создаём контейнер для текста
    response_container = st.empty()
    full_response = ""

    # стриминг
    stream = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": user_input}],
        stream=True,
    )

    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            delta = chunk.choices[0].delta.content
            full_response += delta
            response_container.markdown(full_response)  # обновляем на странице

    st.success("✅ Поток завершён")
