from typing import override
from chatbot.chatbot_base import BaseChatBot
from chatbot.chat_context import ChatContext
from chatbot.chat_history import user_message
from chatbot.services.llm import LLM
from chatbot.services.local_llm import LocalLLM


# Chat bot implementation
class ChatBot(BaseChatBot):
    """Uses an LLM"""

    def __init__(self):
        # LLM is created once, at chatbot construction
        self._llm = LocalLLM(
            temperature=2,   # Massive dispersed answer
            top_p=0.9,
            max_tokens=200,  # correct OpenAI parameter
        )

    @override
    def get_answer(self, question: str, ctx: ChatContext) -> str:
        """
        Produce the assistant's reply to the provided user question.
        Can use ctx to emit status updates, which will be displayed in the UI.
        """
        ctx.update_status("🧠 Thinking...")
        # TODO: find out how to create and call an LLM service
        # bonus: create the LLM only once and reuse it here
        # note that the message history contains only the user's question
        messages = [user_message(question)]
        # call the LLM
        response = self._llm.invoke(messages, config=self.get_config(ctx))
        # extract the answer
        answer = str(response.content)


        # TODO: study the structure of the LLM response in the langchain docs
        # https://python.langchain.com/api_reference/core/messages/langchain_core.messages.ai.AIMessage.html
        return answer
