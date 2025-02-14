import logging

logging.basicConfig(level=logging.INFO,
                    filename="agent_execution.log",
                    filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger("Autogen")

chat_history = []




