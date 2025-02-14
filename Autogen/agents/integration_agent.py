from autogen import AssistantAgent
from dotenv import load_dotenv
import os
from logger import logger
from autogen.coding import LocalCommandLineCodeExecutor

load_dotenv()
MODEL = os.getenv("MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

integration_agent = AssistantAgent(
    name="IntegrationAgent",
    system_message=(
        "You are responsible for integrating the frontend and backend."
        " Ensure that React components correctly call the Express.js APIs."
        " Identify and fix any API response mismatches."
        " Once your work is done end with 'TERMINATE'."
    ),
    llm_config={"model": MODEL, "api_key": OPENAI_API_KEY},
    is_termination_msg=lambda x: x.get("content", "").rstrip(".").rstrip().endswith("TERMINATE"),
    code_execution_config={
        # the executor to run the generated code
        "executor": LocalCommandLineCodeExecutor(work_dir="agentcoding"),
    }
)

logger.info("IntegrationAgent initialized to process integration tasks.")