from chatbot.services.llm_service import (
    LLMService
)


class TitleService:

    @staticmethod
    def generate_title(
        first_message
    ):

        prompt = f"""
Generate a short chat title.

Rules:
- Maximum 5 words
- No quotes
- No punctuation
- Return only the title

Message:
{first_message}

Title:
"""

        llm = LLMService.get_llm()

        response = llm.invoke(
            prompt
        )

        return (
            response.content.strip()
        )