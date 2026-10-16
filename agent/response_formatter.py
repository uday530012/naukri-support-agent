class ResponseFormatter:

    def format_application_status(self, tool_result):

        if not tool_result.get("success"):

            return {
                "status": "ERROR",
                "type": "APPLICATION_STATUS",
                "response": tool_result.get(
                    "message",
                    "Unable to find application information."
                ),
                "source": "Application Database",
                "next_action": "Please check your application ID."
            }

        return {
            "status": "SUCCESS",
            "type": "APPLICATION_STATUS",
            "response": (
                f"Your application for "
                f"{tool_result['job']} is currently "
                f"{tool_result['status']}."
            ),
            "source": "Application Database",
            "next_action": (
                "Please wait for the recruitment team "
                "to provide the next update."
            )
        }

    def format_interview_status(self, tool_result):

        if not tool_result.get("success"):

            return {
                "status": "ERROR",
                "type": "INTERVIEW_STATUS",
                "response": tool_result.get(
                    "message",
                    "Unable to find interview information."
                ),
                "source": "Interview Database",
                "next_action": (
                    "Please check your application ID."
                )
            }

        return {
            "status": "SUCCESS",
            "type": "INTERVIEW_STATUS",
            "response": (
                f"Your interview is scheduled on "
                f"{tool_result['date']} at "
                f"{tool_result['time']} "
                f"({tool_result['mode']})."
            ),
            "source": "Interview Database",
            "next_action": (
                "Please be available before the scheduled time."
            )
        }

    def format_ticket(self, tool_result):

        if not tool_result.get("success"):

            return {
                "status": "ERROR",
                "type": "SUPPORT_TICKET",
                "response": tool_result.get(
                    "message",
                    "Unable to create support ticket."
                ),
                "source": "Support Ticket System",
                "next_action": "Please try again."
            }

        return {
            "status": "SUCCESS",
            "type": "SUPPORT_TICKET",
            "response": (
                "Your support request has been "
                "successfully created."
            ),
            "source": "Support Ticket System",
            "next_action": (
                f"Your ticket ID is "
                f"{tool_result['ticket_id']}."
            )
        }

    def format_blocked(self, reason):

        return {
            "status": "BLOCKED",
            "type": "GUARDRAIL",
            "response": (
                "I cannot process this request."
            ),
            "source": "Safety Guardrails",
            "next_action": reason
        }

    def format_rag(self, retrieved_information):

        if not retrieved_information:

            return {
                "status": "NO_RESULT",
                "type": "RAG",
                "response": (
                    "I could not find relevant "
                    "information in the knowledge base."
                ),
                "source": "Knowledge Base",
                "next_action": (
                    "Please try asking the question differently."
                )
            }

        top_result = retrieved_information[0]

        return {
            "status": "SUCCESS",
            "type": "RAG",
            "response": top_result.get(
                "document",
                "Relevant information was found."
            ),
            "source": "Knowledge Base",
            "next_action": (
                "Please review the policy information above."
            )
        }


def main():

    formatter = ResponseFormatter()

    print("=" * 70)
    print("NAUKRI SUPPORT AGENT - STRUCTURED OUTPUT TEST")
    print("=" * 70)

    # --------------------------------------------------
    # TEST 1 - APPLICATION STATUS
    # --------------------------------------------------

    application_result = {
        "success": True,
        "application_id": "APP1001",
        "candidate": "Candidate 1",
        "job": "Python Developer",
        "status": "Under Review"
    }

    result1 = formatter.format_application_status(
        application_result
    )

    print("\nTEST 1 - APPLICATION STATUS")
    print("-" * 70)
    print(result1)

    # --------------------------------------------------
    # TEST 2 - INTERVIEW
    # --------------------------------------------------

    interview_result = {
        "success": True,
        "application_id": "APP1002",
        "date": "2026-10-20",
        "time": "11:00 AM",
        "mode": "Online",
        "status": "Scheduled"
    }

    result2 = formatter.format_interview_status(
        interview_result
    )

    print("\nTEST 2 - INTERVIEW STATUS")
    print("-" * 70)
    print(result2)

    # --------------------------------------------------
    # TEST 3 - SUPPORT TICKET
    # --------------------------------------------------

    ticket_result = {
        "success": True,
        "ticket_id": "TICKET1001",
        "issue": "Unable to update application",
        "status": "Open"
    }

    result3 = formatter.format_ticket(
        ticket_result
    )

    print("\nTEST 3 - SUPPORT TICKET")
    print("-" * 70)
    print(result3)

    # --------------------------------------------------
    # TEST 4 - BLOCKED
    # --------------------------------------------------

    result4 = formatter.format_blocked(
        "Sensitive information detected."
    )

    print("\nTEST 4 - BLOCKED REQUEST")
    print("-" * 70)
    print(result4)


if __name__ == "__main__":
    main()