from typing import override
from langchain_core.prompts import PromptTemplate

from chatbot.chatbot_base import BaseChatBot
from chatbot.chat_context import ChatContext
from chatbot.chat_history import user_message, system_message
from chatbot.services.llm import LLM


class ChatBot(BaseChatBot):
    """Chatbot that can use either a static system prompt or a dynamic prompt template."""

    def __init__(self):
        self._llm = LLM()

        # -----------------------------
        # STATIC PROMPT (default)
        # -----------------------------
        self._static_prompt = """Your role is given by type of user message:
- if it is a question, you have a bubbly personality
- otherwise, you are lazy and slow"""

        # -----------------------------
        # DYNAMIC PROMPT TEMPLATE
        # -----------------------------
        self._dynamic_prompt_template = PromptTemplate.from_template(
            """You are a chatbot whose behavior depends on the input.

User message: "{user_msg}"

Rules:
- If the message ends with '?', respond with a GRUMPY personality.
- Otherwise, respond with a LAZY personality.

Now produce an in-character response."""
        )

        # Default = use static prompt
        self.use_dynamic_prompt = False

    # -----------------------------------------------------------
    # Build dynamic system prompt using LangChain PromptTemplate
    # -----------------------------------------------------------
    def _get_dynamic_prompt(self, question: str) -> str:
        return self._dynamic_prompt_template.format(user_msg=question)

    # -----------------------------------------------------------
    # Decide which system prompt to use
    # -----------------------------------------------------------
    def _get_system_prompt(self, question: str) -> str:
        if self.use_dynamic_prompt:
            return self._get_dynamic_prompt(question)
        return self._static_prompt

    # -----------------------------------------------------------
    # Main logic
    # -----------------------------------------------------------
    @override
    def get_answer(self, question: str, ctx: ChatContext) -> str:
        ctx.update_status("🧠 Thinking...")

        system_prompt = self._get_system_prompt(question)

        messages = [
            system_message(system_prompt),
            user_message(question)
        ]

        response = self._llm.invoke(messages, config=self.get_config(ctx))

        return str(response.content)
