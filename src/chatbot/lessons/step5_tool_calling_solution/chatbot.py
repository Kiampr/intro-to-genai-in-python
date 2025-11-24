import requests
from enum import Enum
import datetime
from zoneinfo import ZoneInfo
from typing import override
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from chatbot.chatbot_base import BaseChatBot
from chatbot.chat_context import ChatContext
from chatbot.chat_history import ChatHistory, assistant_message, user_message
from chatbot.services.llm import LLM


# a tool is a function exposed the LLM
# the model can request it to be called and the answer is returned as the reply
class TimeZone(Enum):
    America_NewYork = "America/New_York"
    Europe_London = "Europe/London"
    Europe_Warsaw = "Europe/Warsaw"
    Europe_Oslo = "Europe/Oslo"


@tool
def convert_time(
    time_24h: datetime.time, from_time_zone: TimeZone, to_time_zone: TimeZone
) -> str:
    """Converts today's time from one time zone to another.
    time: 'HH:MM[:SS]' (no timezone, no 'Z')
    Example: 10:00
    Returns ISO-8601 with offset, plus target time zone in brackets.
    """
    from_tz = ZoneInfo(from_time_zone.value)
    to_tz = ZoneInfo(to_time_zone.value)
    today = datetime.datetime.now(from_tz).date()
    date_time_24h = datetime.datetime.combine(today, time_24h, tzinfo=from_tz)
    return f"{date_time_24h.astimezone(to_tz).isoformat()} [{to_time_zone.value}]"


class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    NOK = "NOK"


@tool
def convert_currency(
    amount: float, from_currency: Currency, to_currency: Currency
) -> float:
    """Converts money between currencies at today's rate."""
    url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency.value}&to={to_currency.value}"
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    data = response.json()
    answer = data["rates"][to_currency.value]
    return answer


# Chat bot implementation
class ChatBot(BaseChatBot):
    """Uses an LLM with tools"""

    def __init__(self):
        # vanilla language model
        llm = LLM()
        # list of tools at the model's disposal - they need to be decorated with @tool
        tools = [convert_time, convert_currency]
        # predefined tool calling agent in LangGraph
        # it resolves tool calls in a loop until none are requested
        self._graph = create_react_agent(model=llm, tools=tools)
        self._chat_history = ChatHistory()

    @override
    def get_answer(self, question: str, ctx: ChatContext) -> str:
        """
        Produce the assistant's reply to the provided user question.
        Can use ctx to emit status updates, which will be displayed in the UI.
        """
        ctx.update_status("🧠 Thinking...")
        # record question in chat history
        self._chat_history.add_message(user_message(question))
        # call the LLM with all historic messages
        # also pass ctx so that the agent can publish status updates on tool calls to the UI
        response = self._graph.invoke(
            {"messages": self._chat_history.messages}, config=self.get_config(ctx)
        )
        # extract the answer
        # multiple messages may have been generated, the last one is the final response
        answer = str(response["messages"][-1].content)
        # record answer in chat history
        self._chat_history.add_message(assistant_message(answer))

        return answer
