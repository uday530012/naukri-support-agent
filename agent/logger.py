import json
import logging
import os
import re
import uuid
from datetime import datetime, timezone


class AgentLogger:

    def __init__(self, log_file="logs/agent.jsonl"):

        # Create logs directory
        log_directory = os.path.dirname(log_file)

        if log_directory:
            os.makedirs(log_directory, exist_ok=True)

        self.log_file = log_file

        # Keep a normal Python logger for application errors
        self.logger = logging.getLogger("NaukriSupportAgent")

        if not self.logger.handlers:

            self.logger.setLevel(logging.INFO)

            file_handler = logging.FileHandler(
                "logs/agent_runtime.log",
                encoding="utf-8"
            )

            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s"
            )

            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    # ========================================================
    # PHONE NUMBER MASKING
    # ========================================================

    @staticmethod
    def mask_sensitive_text(text):

        if text is None:
            return ""

        text = str(text)

        # +91 9876543210
        text = re.sub(
            r"(\+91[\s-]*)\d{10}",
            r"\1**********",
            text
        )

        # 9876543210
        text = re.sub(
            r"\b\d{10}\b",
            "**********",
            text
        )

        # 98765 43210
        text = re.sub(
            r"\b\d{5}\s\d{5}\b",
            "**********",
            text
        )

        return text

    # ========================================================
    # JSONL REQUEST LOGGER
    # ========================================================

    def log_request(
        self,
        user_message,
        response_type=None,
        selected_tool=None,
        guardrail_status=None,
        status="SUCCESS",
        trace_id=None,
        duration_ms=None,
        method=None,
        path=None,
        status_code=None
    ):

        if trace_id is None:
            trace_id = str(uuid.uuid4())

        masked_message = self.mask_sensitive_text(user_message)

        log_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "trace_id": trace_id,
            "method": method,
            "path": path,
            "duration_ms": duration_ms,
            "status_code": status_code,
            "request_text": masked_message,
            "response_type": response_type,
            "selected_tool": selected_tool,
            "guardrail_status": guardrail_status,
            "status": status
        }

        # Remove fields that were not supplied
        log_record = {
            key: value
            for key, value in log_record.items()
            if value is not None
        }

        # Write ONE JSON object per line
        with open(
            self.log_file,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                json.dumps(
                    log_record,
                    ensure_ascii=False
                )
                + "\n"
            )

        return trace_id

    # ========================================================
    # ERROR LOGGER
    # ========================================================

    def log_error(self, message):

        masked_message = self.mask_sensitive_text(message)

        self.logger.error(masked_message)


# ============================================================
# LOGGER TEST
# ============================================================

if __name__ == "__main__":

    logger = AgentLogger()

    trace_id = logger.log_request(
        user_message="What is the notice period?",
        response_type="RAG",
        selected_tool="rag",
        guardrail_status="ALLOWED",
        status="SUCCESS",
        method="POST",
        path="/chat",
        status_code=200,
        duration_ms=125
    )

    logger.log_request(
        user_message="My phone number is 9876543210",
        response_type="GUARDRAIL",
        selected_tool=None,
        guardrail_status="BLOCKED",
        status="BLOCKED",
        method="POST",
        path="/chat",
        status_code=200,
        duration_ms=15
    )

    print("=" * 70)
    print("JSONL LOGGER TEST")
    print("=" * 70)

    print("Logger initialized successfully.")
    print("Log file: logs/agent.jsonl")
    print(f"Trace ID: {trace_id}")