from autogen import AssistantAgent
from autogen.coding import LocalCommandLineCodeExecutor
from dotenv import load_dotenv
import os
from logger import logger

load_dotenv()
MODEL = os.getenv("MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

frontend_agent = AssistantAgent(
    name="FrontendAgent",
    # system_message=(
    #     "You are a frontend developer specializing in React Vite and TypeScript."
    #     " Your task is to generate modular, well-structured React components following best practices."
    #     " Follow these rules:\n"
    #     "- Use functional components and React Hooks.\n"
    #     "- Ensure clean and maintainable code with proper indentation.\n"
    #     "- Avoid inline styles; use CSS modules or styled-components.\n"
    #     "- Use TypeScript with correct typings and interface definitions.\n"
    #     "- If state management is required, use React Context API or Redux.\n"
    #     "- Ensure accessibility (ARIA attributes where needed).\n"
    #     "- Do not include unnecessary explanations, only provide the React component.\n\n"
    #     "When responding, provide only the code, without any additional comments or explanations."
    # ),
    system_message=(
        "You are a frontend developer. Your ONLY task is to generate the requested React + TypeScript code."
        " Generate well-structured UI components following best practices."
        " DO NOT engage in unnecessary conversations."
        " Once your code is generated, send it for validation and include 'TERMINATE'."
    ),
    # max_consecutive_auto_reply=1,  # Prevents looping
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    llm_config={
        "model": MODEL,
        "api_key": OPENAI_API_KEY
    },
    code_execution_config={
        # the executor to run the generated code
        "executor": LocalCommandLineCodeExecutor(work_dir="agentcoding"),
    }
)

logger.info("FrontendAgent initialized to process frontend development tasks.")
