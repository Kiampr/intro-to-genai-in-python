from typing import override
from chatbot.chatbot_base import BaseChatBot
from chatbot.chat_context import ChatContext


# Chat bot implementation
class ChatBot(BaseChatBot):
    """Uses an LLM"""

    @override
    def get_answer(self, question: str, ctx: ChatContext) -> str:
        """
        Produce the assistant's reply to the provided user question.
        Can use ctx to emit status updates, which will be displayed in the UI.
        """
        ctx.update_status("🧠 Thinking...")
        # TODO: find out how to create and call an LLM service
        # bonus: create the LLM only once and reuse it here
        answer = "???"

        # TODO: study the structure of the LLM response in the langchain docs
        # https://python.langchain.com/api_reference/core/messages/langchain_core.messages.ai.AIMessage.html
        return answer
