import os
from openai import OpenAI
from dotenv import load_dotenv  # Load environment variables from .env file

load_dotenv()  # take environment variables from .env file


# Инициализация клиента
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI()


# Базовый класс Agent
class Agent:
    def __init__(self, name: str):
        self.name = name


# Агент с LLM
class LLMAgent(Agent):
    def __init__(self, name: str, model: str = "gpt-5-nano"):
        super().__init__(name)
        self.model = model

    def think(self, input_data: str) -> str:
        """Использует LLM для принятия решений."""
        response = client.chat.completions.create(
            model=self.model, messages=[{"role": "user", "content": input_data}]
        )
        return response.choices[0].message.content


# --- Использование ---
if __name__ == "__main__":
    agent = LLMAgent("Мой Агент")
    reply = agent.think("Придумай слоган для кофейни в стиле хай-тек")
    print("Ответ агента:", reply)
