class ToolRouter:

    def __init__(self):

        print("Tool Router initialized.")

    # ==================================================
    # SELECT TOOL
    # ==================================================

    def select_tool(self, message):

        message_lower = message.lower()

        # --------------------------------------------------
        # APPLICATION STATUS
        # --------------------------------------------------

        application_keywords = [
            "application status",
            "status of my application",
            "status of application",
            "application progress",
            "application update",
            "check my application",
            "check application",
            "track my application",
            "track application"
        ]

        # Application ID itself is a strong signal
        if "app" in message_lower:

            import re

            if re.search(
                r"\bAPP\d+\b",
                message.upper()
            ):

                # If the message contains status-related wording,
                # route to application status.
                status_keywords = [
                    "status",
                    "application",
                    "submitted",
                    "progress",
                    "update",
                    "track",
                    "check"
                ]

                if any(
                    keyword in message_lower
                    for keyword in status_keywords
                ):

                    return "application_status"

        if any(
            keyword in message_lower
            for keyword in application_keywords
        ):

            return "application_status"

        # --------------------------------------------------
        # INTERVIEW STATUS
        # --------------------------------------------------

        interview_keywords = [
            "interview",
            "interview date",
            "interview time",
            "interview schedule",
            "interview scheduled",
            "interview status"
        ]

        if any(
            keyword in message_lower
            for keyword in interview_keywords
        ):

            return "interview_status"

        # --------------------------------------------------
        # SUPPORT TICKET
        # --------------------------------------------------

        ticket_keywords = [
            "problem",
            "issue",
            "unable",
            "cannot",
            "can't",
            "not working",
            "error",
            "failed",
            "failure",
            "unable to update",
            "unable to apply"
        ]

        if any(
            keyword in message_lower
            for keyword in ticket_keywords
        ):

            return "create_ticket"

        # --------------------------------------------------
        # DEFAULT → RAG
        # --------------------------------------------------

        return "rag"

    # ==================================================
    # EXECUTE TOOL
    # ==================================================

    def execute_tool(
        self,
        tool_name,
        application_id=None,
        issue=None
    ):

        from agent.tools import NaukriTools

        tools = NaukriTools()

        # --------------------------------------------------
        # APPLICATION STATUS
        # --------------------------------------------------

        if tool_name == "application_status":

            return tools.check_application_status(
                application_id
            )

        # --------------------------------------------------
        # INTERVIEW STATUS
        # --------------------------------------------------

        elif tool_name == "interview_status":

            return tools.check_interview_status(
                application_id
            )

        # --------------------------------------------------
        # SUPPORT TICKET
        # --------------------------------------------------

        elif tool_name == "create_ticket":

            return tools.create_support_ticket(
                issue
            )

        # --------------------------------------------------
        # UNKNOWN TOOL
        # --------------------------------------------------

        return {
            "status": "error",
            "message": "Unknown tool selected."
        }


# ==========================================================
# TEST
# ==========================================================

def main():

    router = ToolRouter()

    test_cases = [
        "What is my application status?",
        "What is the status of APP1003?",
        "Check APP1001",
        "What is APP1002 application status?",
        "When is my interview scheduled?",
        "I am unable to update my application.",
        "What is the notice period?"
    ]

    print("\n")
    print("=" * 70)
    print("TOOL ROUTER TEST")
    print("=" * 70)

    for message in test_cases:

        selected_tool = router.select_tool(
            message
        )

        print("\nMessage:")
        print(message)

        print("Selected Tool:")
        print(selected_tool)


if __name__ == "__main__":

    main()