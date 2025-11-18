# Introduction to Gen-AI in Python

This is a tutorial for those looking to get started programming GenAI-based applications in Python.

Lesson | Links
---    |---
Introduction | 📖 [Exercise](/src/chatbot/lessons/step0_intro/README.md)
Prompting | 📖 [Exercise](/src/chatbot/lessons/step1_prompting/README.md) ✅ [Solution](/src/chatbot/lessons/step1_prompting_solution/README.md)
System instructions | 📖 [Exercise](/src/chatbot/lessons/step2_system_prompt/README.md) ✅ [Solution](/src/chatbot/lessons/step2_system_prompt_solution/README.md)
Tracking conversation history | 📖 [Exercise](/src/chatbot/lessons/step3_conversation_history/README.md) ✅ [Solution](/src/chatbot/lessons/step3_conversation_history_solution/README.md)
Structured outputs | 📖 [Exercise](/src/chatbot/lessons/step4_structured_outputs/README.md) ✅ [Solution](/src/chatbot/lessons/step4_structured_outputs_solution/README.md)
Tool calling | 📖 [Exercise](/src/chatbot/lessons/step5_tool_calling/README.md) ✅ [Solution](/src/chatbot/lessons/step5_tool_calling_solution/README.md)
Custom agent | 📖 [Exercise](/src/chatbot/lessons/step6_custom_agent/README.md) ✅ [Solution](/src/chatbot/lessons/step6_custom_agent_solution/README.md)

A basic [`streamlit`](https://docs.streamlit.io/get-started) chat UI is provided, so that the lessons can solely focus on the chatbot logic.

![Chat UI](/images/ui.png)

## Getting started

1. Clone this repo.

1. Install a recent version of Python 3.

    You can use `winget` within `powershell`

    ```powershell
    winget install --id Python.Python.3.13 --version 3.13.3 --scope user
    ```

    Or [download](https://www.python.org/downloads/release/python-3133/) and install somewhere accessible e.g. `%APPDATA%`.

1. Install poetry, which will manage the project's Python package dependencies.

    ```bash
    pip install poetry
    ```

1. Use poetry to setup the dependencies by running the following command at the git clone location

    ```bash
    poetry install
    ```

1. Install Ollama server, which will be used to launch local language models.

    Using `winget`

    ```powershell
    winget install --id Ollama.Ollama --scope user
    ```

    Or [download](https://github.com/ollama/ollama/releases/tag/v0.12.3) and install somewhere accessible e.g. `%APPDATA%`.

1. Start the app by running the command below in the clone location

    ```bash
    poetry run genai-chat
    ```

    If you make code changes to the chatbot logic while the app is running, you need to kill and restart it. Do this by issuing Ctrl-C in the terminal - simply closing the webpage is not enough, since the streamlit server continues to run!

1. Alternatively, each lesson can be run in console mode

    ```bash
    poetry run lesson-5
    ```

    or a corresponding solution

    ```bash
    poetry run lesson-5-solution
    ```
