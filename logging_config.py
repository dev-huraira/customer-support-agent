import logging
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler("agent.log"),
            logging.StreamHandler(),
        ],
    )
logger = logging.getLogger("customer_support_agent")