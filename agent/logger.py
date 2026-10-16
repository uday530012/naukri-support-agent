import logging
import os
from datetime import datetime


class AgentLogger:

    def __init__(self, log_file="logs/agent.log"):

        # Create logs directory if it does not exist
        log_directory = os.path.dirname(log_file)

        if log_directory:
            os.makedirs(log_directory, exist_ok=True)

        self.logger = logging.getLogger("NaukriSupportAgent")

        # Prevent duplicate handlers
        if not self.logger.handlers:

            self.logger.setLevel(logging.INFO)

            file_handler = logging.FileHandler(
                log_file,
                encoding="utf-8"
            )

            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s"
            )

            file_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)

    def log_request(
        self,
        user_message,
        response_type=None,
        selected_tool=None,
        guardrail_status=None,
        status="SUCCESS"
    ):

        self.logger.info(
            "REQUEST | "
            f"message={user_message} | "
            f"response_type={response_type} | "
            f"tool={selected_tool} | "
            f"guardrail={guardrail_status} | "
            f"status={status}"
        )

    def log_error(self, error_message):

        self.logger.error(
            f"ERROR | {error_message}"
        )


if __name__ == "__main__":

    logger = AgentLogger()

    logger.log_request(
        user_message="What is the notice period?",
        response_type="RAG",
        selected_tool="rag",
        guardrail_status="ALLOWED"
    )

    logger.log_request(
        user_message="What is my application status?",
        response_type="APPLICATION_STATUS",
        selected_tool="application_status",
        guardrail_status="ALLOWED"
    )

    logger.log_request(
        user_message="Give me the candidate password.",
        response_type="GUARDRAIL",
        selected_tool=None,
        guardrail_status="BLOCKED",
        status="BLOCKED"
    )

    logger.log_error(
        "Example error message"
    )

    print("=" * 70)
    print("LOGGER TEST")
    print("=" * 70)

    print("Logging system initialized successfully.")
    print("Log file: logs/agent.log")