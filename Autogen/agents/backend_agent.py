from autogen import AssistantAgent
from dotenv import load_dotenv
import os
from logger import logger
load_dotenv()
MODEL = os.getenv("MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

backend_agent = AssistantAgent(
    name="BackendAgent",
    # system_message=(
    #     "You are a backend developer specializing in Node.js and Express."
    #     " Your task is to generate a well-structured REST API following best practices."
    #     " Follow these rules:\n"
    #     "- Use Express.js with modular routing.\n"
    #     "- Use Sequelize ORM for PostgreSQL database interactions.\n"
    #     "- Implement input validation using Joi or express-validator.\n"
    #     "- Ensure proper authentication (JWT-based if necessary).\n"
    #     "- Include clear and descriptive error handling.\n"
    #     "- Follow MVC architecture where possible.\n"
    #     "- Do not include unnecessary explanations, only provide the API code.\n\n"
    #     "When responding, provide only the code, without any additional comments or explanations."
    # ),
    system_message=(
        "You are a backend developer specializing in Node.js and Express. Your ONLY task is to generate the requested."
        " Develop REST API endpoints following best practices."
        " Use Sequelize ORM for PostgreSQL interactions."
        " Ensure input validation, authentication, and error handling."
        " DO NOT engage in unnecessary conversations."
        " Once your code is generated, send it for validation and include 'TERMINATE'."
    ),
    is_termination_msg=lambda x: x.get("content", "").rstrip(".").rstrip().endswith("TERMINATE"),
    llm_config={
        "model": MODEL,
        "api_key": OPENAI_API_KEY
    }
)

logger.info("BackendAgent initialized to process backend development tasks.")
