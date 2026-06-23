from langchain_groq import ChatGroq

from chatbot.config import GROQ_API_KEY


class LLMService:

    @staticmethod
    def get_llm():

        llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model="llama-3.1-8b-instant",
            temperature=0
        )

        return llm