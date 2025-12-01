import time
from typing import override
from chatbot.chatbot_base import BaseChatBot
from chatbot.chat_context import ChatContext


# Chat bot implementation
class ChatBot(BaseChatBot):
    """Repeats the user message"""

    @override
    def get_answer(self, question: str, ctx: ChatContext) -> str:
        """
        Produce the assistant's reply to the provided user question.
        Can use ctx to emit status updates, which will be displayed in the UI.
        """
        ctx.update_status("🔍 Analyzing user question...")
        time.sleep(0.5)

        ctx.update_status("🤔 Reasoning...")
        time.sleep(2)
        answer = f"Hello there! I am not programmed to answer to: `{question}`"

        return answer
