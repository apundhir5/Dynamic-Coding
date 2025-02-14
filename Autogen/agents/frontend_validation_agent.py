from autogen import AssistantAgent
from dotenv import load_dotenv
import os
from logger import logger
from autogen.coding import LocalCommandLineCodeExecutor

load_dotenv()
MODEL = os.getenv("MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

frontend_validation_agent = AssistantAgent(
    name="FrontendValidationAgent",
    # system_message=(
    #     "You are a frontend QA specialist."
    #     " Validate React + TypeScript components for correctness, accessibility, and performance."
    #     " If issues are found, provide fixes and send back to FrontendAgent."
    # ),
    system_message=(
        "You are responsible for validating React + TypeScript components."
        " Only provide validation feedback, and DO NOT engage in unnecessary discussions."
        " If validation passes or fails, simply return the results and send 'TERMINATE'."
    ),
    # max_consecutive_auto_reply=1,  # Avoids multiple unnecessary replies
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    llm_config={"model": MODEL, "api_key": OPENAI_API_KEY},
    code_execution_config={
        # the executor to run the generated code
        "executor": LocalCommandLineCodeExecutor(work_dir="agentcoding"),
    }
)

logger.info("FrontendValidationAgent initialized to process frontend validation tasks.")