from autogen import AssistantAgent
from dotenv import load_dotenv
import os
from logger import logger
load_dotenv()
MODEL = os.getenv("MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

requirement_agent = AssistantAgent(
    name="RequirementAgent",
    # description="You are a software architect. Your role is to break down high-level application requirements into structured frontend and backend tasks.",
    system_message=(
        "You are a software requirements analyst."
        " Given a high-level user request, break it down into structured tasks."
        " Clearly separate frontend and backend requirements and send tasks to the correct agents."
    ),
    llm_config={
        "model": MODEL,
        "api_key": OPENAI_API_KEY
    }
)

logger.info("RequirementAgent initialized to process high-level tasks.")
