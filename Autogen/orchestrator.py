from agents.requirement_agent import requirement_agent
from agents.frontend_agent import frontend_agent
from agents.backend_agent import backend_agent
from agents.frontend_validation_agent import frontend_validation_agent
from agents.backend_validation_agent import backend_validation_agent
from agents.integration_agent import integration_agent
from agents.deployment_agent import deployment_agent
from Autogen.logger import logger, chat_history  # Import chat history list

# Function to log message exchanges and store them
def log_and_store_chat(sender, recipient, message, max_turns=None):
    log_entry = f"{sender.name} → {recipient.name if recipient else 'None'}: {message}"
    logger.info(log_entry)
    chat_history.append(log_entry)  # Store chat in memory
    sender.initiate_chat(recipient, message, verbose=True, max_turns=max_turns)

logger.info("STARTING ORCHESTRATOR--------------------------------")

MAIN_TASK = "Build a user authentical system with React frontend and Node.js backend."
# MAIN_TASK = "Build a python function that takes a string and returns the string in reverse order."

# Step 1: Requirement Breakdown (Pass Main Task)
requirement_agent.initiate_chat(
    recipient=frontend_agent,
    message=f"The user wants: {MAIN_TASK}."
            " Your task is to define the required UI components, state management, and styling approach."
            " Generate a TypeScript + React login and signup page following best practices.",
    verbose=True,
    max_turns=1
)

requirement_agent.initiate_chat(
    recipient=backend_agent,
    message=f"The user wants: {MAIN_TASK}."
            " Your task is to define authentication strategy, database schema, and API endpoints."
            " Implement a secure user authentication system using Express.js and Sequelize.",
    verbose=True,
    max_turns=1
)

# Step 2: Generate Frontend & Backend Code
frontend_agent.initiate_chat(
    recipient=frontend_validation_agent,
    message="Validate this React login and signup page.",
    verbose=True
)

frontend_validation_result = frontend_validation_agent.last_message(frontend_agent)["content"]

if "error" in frontend_validation_result.lower():
    print(f"Fix these frontend issues: {frontend_validation_result}")
    # frontend_validation_agent.initiate_chat(
    #     recipient=debugging_agent,
    #     message=f"Fix these frontend issues: {frontend_validation_result}"
    # )
else:
    print(f"Frontend validation passed: {frontend_validation_result}")

backend_agent.initiate_chat(
    recipient=backend_validation_agent,
    message="Validate this Express.js authentication API.",
    verbose=True
)

backend_validation_result = backend_validation_agent.last_message(backend_agent)["content"]
if "error" in backend_validation_result.lower():
    print(f"Fix these backend issues: {backend_validation_result}")
else:
    print(f"Backend validation passed: {backend_validation_result}")

# Step 3: Integration
integration_agent.initiate_chat(
    recipient=frontend_agent,
    message="Ensure frontend correctly interacts with backend authentication API.",
    verbose=True
)

# recipient cannot be none, throwing errrors. TODO: fix this
# # Step 4: Deployment
# deployment_agent.initiate_chat(
#     recipient=None,
#     message="Deploy the validated application.",
#     verbose=True
# )


# Step 5: Print Chat History After Execution
print("\n🚀 **Complete Agent Chat History** 🚀")
# logger.info("🚀 AutoGen development workflow completed successfully!")
