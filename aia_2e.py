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


class Agent:
    def __init__(self, name: str):
        self.name = name


class LLMAgent(Agent):
    def __init__(self, name: str, model: str = model):
        super().__init__(name)
        self.model = model

    def think_stream(self, input_data: str, on_chunk=None) -> str:
        """Стриминговый ответ LLM"""
        full_response = ""
        stream = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": input_data}],
            stream=True,
        )

        if on_chunk is None:

            def on_chunk(text: str):
                print(text, end="", flush=True)

        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                delta = chunk.choices[0].delta.content
                on_chunk(delta)
                full_response += delta

        return full_response


def get_unique_filepath(base_dir: str, filename: str) -> str:
    """
    Проверяет, существует ли файл.
    Если существует — добавляет _1, _2 и т.д.
    """
    base, ext = os.path.splitext(filename)
    candidate = os.path.join(base_dir, filename)
    counter = 1
    while os.path.exists(candidate):
        candidate = os.path.join(base_dir, f"{base}_{counter}{ext}")
        counter += 1
    return candidate


# --- Использование ---
if __name__ == "__main__":
    agent = LLMAgent("Мой Агент")

    # директория, где лежит скрипт
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = get_unique_filepath(current_dir, "agent_output.txt")

    print("\n=== Вариант 2: поток в файл с авто-нумерацией ===")
    with open(file_path, "w", encoding="utf-8") as f:
        reply_file = agent.think_stream(
            "Напиши короткий тост о дружбе.", on_chunk=lambda text: f.write(text)
        )
    print(f"\nОтвет сохранён в: {file_path}")
