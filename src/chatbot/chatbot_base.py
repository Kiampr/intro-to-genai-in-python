from abc import ABC, abstractmethod
import inspect
from pathlib import Path
from langchain_core.runnables import RunnableConfig
from chatbot.chat_context import ChatContext


class BaseChatBot(ABC):
    """
    Chatbot base class serving as blueprint for all implementations.
    """

    @classmethod
    def get_name(cls) -> str:
        """Returns the name of the directory holding the implementation, e.g. step0_intro"""
        return Path(inspect.getfile(cls)).parent.name

    @classmethod
    def get_description(cls) -> str:
        """Returns the description of the implementation, extracted from the doccomments"""
        return inspect.getdoc(cls) or ""

    @classmethod
    def get_config(cls, ctx: ChatContext, thread_id: str | None = None):
        if thread_id is None:
            thread_id = cls.get_name()
        return RunnableConfig(
            configurable={"thread_id": thread_id},
            callbacks=[ctx],
            recursion_limit=100,
        )

    @abstractmethod
    def get_answer(self, question: str, ctx: ChatContext) -> str:
        """
        Produce the assistant's reply to the provided user question.
        Can use ctx to emit status updates, which will be displayed in the UI.
        """
        raise NotImplementedError
