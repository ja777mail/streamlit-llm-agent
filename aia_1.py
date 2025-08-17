#       -      -       https://external.software/archives/20335       -      -      #
# Реализация ИИ-агента на Python: Пошаговое руководство
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


# Создание базового класса агента с основными методами (восприятие, мышление, действие)
class Agent:
    """Базовый класс для ИИ-агента."""

    def __init__(self, name: str):
        self.name = name

    def perceive(self, environment: str) -> str:
        """Воспринимает окружающую среду."""
        print(f"{self.name}: Воспринимаю {environment}")
        return environment

    def think(self, input_data: str) -> str:
        """Обрабатывает информацию и принимает решения."""
        print(f"{self.name}: Думаю о {input_data}")
        return f"Результат мышления на основе {input_data}"

    def act(self, action: str) -> None:
        """Выполняет действие."""
        print(f"{self.name}: Действую - {action}")


#       =      =       =      =      #

# Интеграция с OpenAI API для использования больших языковых моделей (LLM)
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


class LLMAgent(Agent):
    def __init__(self, name: str, model: str = "gpt-5-mini"):
        super().__init__(name)
        self.model = model

    def think(self, input_data: str) -> str:
        """Использует LLM для принятия решений."""
        response = openai.ChatCompletion.create(
            model=self.model, messages=[{"role": "user", "content": input_data}]
        )
        return response["choices"][0]["message"]["content"]


#       =      =       =      =      #

# Реализация механизмов памяти и базы знаний с использованием ChromaDB или других векторных баз данных
import chromadb


class ChromaAgent(LLMAgent):
    def __init__(self, name: str, model: str = "gpt-5-mini"):
        super().__init__(name, model)
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(name=f"{name}_memory")

    def remember(self, data: str) -> None:
        """Сохраняет информацию в векторной базе данных."""
        self.collection.add(
            documents=[data], ids=[f"{self.name}_{len(self.collection.get()['ids'])}"]
        )

    def recall(self, query: str, n_results: int = 3) -> List[str]:
        """Извлекает релевантную информацию из векторной базы данных."""
        results = self.collection.query(query_texts=[query], n_results=n_results)
        return results["documents"][0]

    def think(self, input_data: str) -> str:
        """Использует память для принятия решений."""
        relevant_memories = self.recall(input_data)
        context = f"Ранее сохраненная информация: {relevant_memories}. Текущий запрос: {input_data}"
        return super().think(context)


#       =      =       =      =      #
