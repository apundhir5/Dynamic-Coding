from autogen import AssistantAgent
from dotenv import load_dotenv
import os
from logger import logger
from autogen.coding import LocalCommandLineCodeExecutor

load_dotenv()
MODEL = os.getenv("MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

deployment_agent = AssistantAgent(
    name="DeploymentAgent",
    system_message=(
        "You are a DevOps engineer. Deploy the application to production."
        " Ensure the frontend is deployed to Vercel/Netlify and the backend is deployed to AWS/DigitalOcean."
        " Once deployment is complete end with 'TERMINATE'."
    ),
    llm_config={"model": MODEL, "api_key": OPENAI_API_KEY},
    is_termination_msg=lambda x: x.get("content", "").rstrip(".").rstrip().endswith("TERMINATE"),
    code_execution_config={
        # the executor to run the generated code
        "executor": LocalCommandLineCodeExecutor(work_dir="agentcoding"),
    }
)

logger.info("DeploymentAgent initialized to process deployment tasks.")