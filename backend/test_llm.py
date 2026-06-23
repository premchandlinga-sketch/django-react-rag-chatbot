from chatbot.services.llm_service import (
    LLMService
)

llm = LLMService.get_llm()

response = llm.invoke(
    "What is machine learning?"
)

print(response.content)