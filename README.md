# LLM based Prototype Generator

A LLM based system that automatically generates frontend and backend prototypes from natural language requirements. The system uses a multi-agent approach to break down requirements, generate code, and validate the implementation.

## Features

- Automatic requirement parsing and separation into frontend/backend specifications
- Independent frontend and backend code generation
- Code validation with feedback
- Iteration limits to prevent infinite loops
- Modular architecture using LangGraph's StateGraph

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