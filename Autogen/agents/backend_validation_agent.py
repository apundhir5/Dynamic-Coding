from autogen import AssistantAgent
from dotenv import load_dotenv
import os
from logger import logger
from autogen.coding import LocalCommandLineCodeExecutor

load_dotenv()
MODEL = os.getenv("MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

backend_validation_agent = AssistantAgent(
    name="BackendValidationAgent",
    system_message=(
        "You are a backend QA specialist."
        " Validate Express.js API endpoints for security, performance, and correctness."
        " Ensure input validation, JWT authentication, and SQL query optimization."
        " Only provide validation feedback, and DO NOT engage in unnecessary discussions."
        " If validation passes or fails, simply return the results and send 'TERMINATE'."
    ),
    is_termination_msg=lambda x: x.get("content", "").rstrip(".").rstrip().endswith("TERMINATE"),
    llm_config={"model": MODEL, "api_key": OPENAI_API_KEY},
    code_execution_config={
        # the executor to run the generated code
        "executor": LocalCommandLineCodeExecutor(work_dir="agentcoding"),
    }
)

logger.info("BackendValidationAgent initialized to process backend validation tasks.")
