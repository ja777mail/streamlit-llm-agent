import os
from openai import OpenAI
from dotenv import load_dotenv  # Load environment variables from .env file

load_dotenv()  # take environment variables from .env file

# В новом SDK можно сделать стриминг так, что токены будут приходить постепенно (как будто модель «печатает»).
# Вот версия, где агент печатает текст сразу в консоль (реальное время) и одновременно собирает полный ответ в строку, чтобы можно было использовать его дальше:
# Инициализация клиента
client = OpenAI()
model = "gpt-5-nano"


# Базовый класс Agent
class Agent:
    def __init__(self, name: str):
        self.name = name


# Агент с LLM
class LLMAgent(Agent):
    def __init__(self, name: str, model: str = "gpt-4.1-mini"):
        super().__init__(name)
        self.model = model

    def think_stream(self, input_data: str) -> str:
        """Стриминговый ответ LLM: печатает в реальном времени и возвращает полный текст"""
        full_response = ""

        stream = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": input_data}],
            stream=True,
        )

        print(f"\n🤖 {self.name} думает:\n")
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                delta = chunk.choices[0].delta.content
                print(delta, end="", flush=True)  # печатаем кусочек сразу
                full_response += delta

        print("\n\n--- Поток завершён ---")
        return full_response


# --- Использование ---
if __name__ == "__main__":
    agent = LLMAgent("Мой Агент")
    # 📌 Что будет происходить:
    # В консоль агент будет «печатать» ответ в реальном времени.
    # После завершения генерации весь текст будет собран в переменной reply.
    reply = agent.think_stream(
        "Напиши короткий рассказ о человеке, который научился чувствовать. Используй не более 50 слов."
    )
    print("\nПолный ответ агента (собранный):", reply)
