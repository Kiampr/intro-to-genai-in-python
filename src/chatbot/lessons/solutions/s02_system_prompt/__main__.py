from chatbot.utils.console import console
from .chatbot import ChatBot
from chatbot.utils.logging import configure_logging

configure_logging()
chatbot = ChatBot()


def main():
    console(chatbot)


if __name__ == "__main__":
    main()
