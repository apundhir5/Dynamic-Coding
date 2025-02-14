from autogen import AssistantAgent
from dotenv import load_dotenv
import os

load_dotenv()
MODEL = os.getenv("MODEL")

debugging_agent = AssistantAgent(
    name="DebuggingAgent",
    system_message="You are an expert in debugging. Refine and fix code errors until the ValidationAgent approves the implementation.",
    llm_config={"model": MODEL}
)
