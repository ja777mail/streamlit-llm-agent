# Отлично 🙌 Тогда вот версия с историей чата (chat history) — теперь можно вести полноценный диалог:
# Теперь:
# - Каждое новое сообщение добавляется в историю.
# - История хранится в st.session_state.messages.
# - После отправки обновляется весь диалог.

# Тогда давай сделаем красиво — в стиле чата (мессенджера). Streamlit позволяет рендерить HTML, поэтому мы обернём сообщения в «пузырьки» с разным фоном.
# Теперь:
# - Сообщения выводятся как пузырьки (user справа, ассистент слева).
# - Цвета похожи на WhatsApp: зелёный для пользователя, серый для ассистента.

# Добавим автопрокрутку вниз — чтобы чат всегда показывал последние сообщения (как в мессенджере).
# Теперь:
# - История чата в прокручиваемом контейнере (500px).
# - При каждом новом сообщении страница автопрокручивается вниз.

# Делаем так, чтобы ответы ассистента рендерились как Markdown (со списками, кодом, заголовками и т.п.).
# Теперь:
# - Пользовательские сообщения — остаются в зелёных пузырях.
# - Ответы ассистента — красиво отображаются как Markdown (например, с блоками кода python ... или списками).

import os
import streamlit as st
from openai import OpenAI

# Читаем API ключ
api_key = os.environ.get("OPENAI_API_KEY") or st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="LLM Chat", layout="centered")
st.title("💬 Мини LLM агент")

# CSS стили для «пузырьков»
st.markdown(
    """
    <style>
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 15px;
        margin: 5px 0;
        max-width: 80%;
        word-wrap: break-word;
        display: inline-block;
        font-size: 16px;
    }
    .user-bubble {
        background-color: #DCF8C6;
        margin-left: auto;
        text-align: right;
    }
    .assistant-bubble {
        background-color: #F1F0F0;
        margin-right: auto;
        text-align: left;
        width: 100%;
    }
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Инициализируем историю чата
if "messages" not in st.session_state:
    st.session_state.messages = []

# Контейнер для чата
chat_box = st.container()

with chat_box:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="chat-bubble user-bubble">{msg["content"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            # 👉 Ассистентский текст рендерим через Markdown
            with st.container():
                st.markdown(
                    f'<div class="chat-bubble assistant-bubble">',
                    unsafe_allow_html=True,
                )
                st.markdown(msg["content"])  # поддержка Markdown
                st.markdown("</div>", unsafe_allow_html=True)
    # 👇 скроллим в конец
    st.markdown('<div id="chat-end"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <script>
        var chatEnd = document.getElementById("chat-end");
        if (chatEnd) {
            chatEnd.scrollIntoView({behavior: "smooth"});
        }
        </script>
    """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Поле для ввода
prompt = st.text_input("Введите сообщение:", key="input")

# Кнопка
if st.button("Отправить"):
    if prompt.strip():
        # Добавляем сообщение пользователя
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("Генерация ответа..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini", messages=st.session_state.messages
            )
            reply = response.choices[0].message.content

            # Добавляем ответ ассистента
            st.session_state.messages.append({"role": "assistant", "content": reply})

        st.rerun()
    else:
        st.warning("Введите текст перед отправкой!")
