# LLM based Prototype Generator

A LLM based system that automatically generates frontend and backend prototypes from natural language requirements. The system uses a multi-agent approach to break down requirements, generate code, and validate the implementation.

## Features

- Automatic requirement parsing and separation into frontend/backend specifications
- Independent frontend and backend code generation
- Code validation with feedback
- Iteration limits to prevent infinite loops
- Modular architecture using LangGraph's StateGraph



## API Keys Required

The following API keys need to be set in your `.env` file:
-  If using openai
- `MODEL`: The LLM model to use (e.g. "gpt-4-turbo")
- `OPENAI_API_KEY`: Your OpenAI API key

-  If using NTTH models
- `NTTH_ID`: NTTH service identifier
- `NTTH-SECRET`: NTTH service secret key
- `NTTH_MODEL`: NTTH model to use (e.g. "GPT-4o")
- `NTTH_PROVIDER`: NTTH provider to use (e.g. "openai")
- `NTTH_BASE_URL`: NTTH base URL (e.g. "https://api.ntth.ai/v1")

-  If using Ollama
- `OLLAMA_MODEL`: Ollama model to use (e.g. "llama3.2")
- `OLLAMA_BASE_URL`: Ollama base URL (e.g. "http://localhost:11434")


## Prerequisites

- Python 3.8+
- Ollama running locally (for LLM)
- Required Python packages:
  - langgraph
  - graphviz
  - langchain
  - langchain_ollama
  - typing_extensions


## Other LLM based implementations to be added:
- Microsoft Autogen
- CrewAI