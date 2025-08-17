import os
from openai import OpenAI
from dotenv import load_dotenv  # Load environment variables from .env file

load_dotenv()  # take environment variables from .env file

# В новом SDK можно сделать стриминг так, что токены будут приходить постепенно (как будто модель «печатает»).
# Вот версия, где агент печатает текст сразу в консоль (реальное время) и одновременно собирает полный ответ в строку, чтобы можно было использовать его дальше:
# Давайте сделаем версию со stream + callback, чтобы можно было легко направлять поток:
# - в консоль (по умолчанию),
# - в GUI (например, tkinter, PyQt, streamlit),
# - в файл или базу данных.

# Инициализация клиента
client = OpenAI()
model = "gpt-5-nano"

from typing import Callable, Optional


# Базовый класс Agent
class Agent:
    def __init__(self, name: str):
        self.name = name


class LLMAgent(Agent):
    def __init__(self, name: str, model: str = model):
        super().__init__(name)
        self.model = model

    def think_stream(
        self, input_data: str, on_chunk: Optional[Callable[[str], None]] = None
    ) -> str:
        """
        Стриминговый ответ LLM.
        :param input_data: запрос пользователя
        :param on_chunk: callback-функция, которая вызывается на каждый кусочек текста
        :return: полный собранный ответ
        """
        full_response = ""

        stream = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": input_data}],
            stream=True,
        )

        if on_chunk is None:
            # по умолчанию печатаем в консоль
            def on_chunk(text: str):
                print(text, end="", flush=True)

        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                delta = chunk.choices[0].delta.content
                on_chunk(delta)
                full_response += delta

        return full_response


# --- Использование ---
if __name__ == "__main__":
    agent = LLMAgent("Мой Агент")

    # 1️⃣ В консоль (по умолчанию)
    print("\n=== Вариант 1: поток в консоль ===")
    reply_console = agent.think_stream("Придумай слоган для кофейни в стиле хай-тек.")
    print("\n\nСобранный ответ:", reply_console)

    # 2️⃣ В файл
    # Путь к текущей директории скрипта
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "agent_output.txt")
    # os.path.abspath(__file__) — полный путь до текущего скрипта.
    # os.path.dirname(...) — директория, где лежит скрипт.
    # os.path.join(..., "agent_output.txt") — файл создаётся именно там.
    print("\n=== Вариант 2: поток в файл (рядом со скриптом) ===")
    with open(file_path, "w", encoding="utf-8") as f:
        reply_file = agent.think_stream(
            "Напиши короткий тост о дружбе.",
            on_chunk=lambda text: f.write(text),  # записываем куски прямо в файл
        )
    print(f"Ответ сохранён в: {file_path}")

    # 3️⃣ В список (например, для GUI)
    print("\n=== Вариант 3: поток в список (для GUI) ===")
    gui_buffer = []
    reply_gui = agent.think_stream(
        "Скажи поэтично о восходе солнца.",
        on_chunk=lambda text: gui_buffer.append(text),
    )
    print("GUI-буфер:", "".join(gui_buffer))
