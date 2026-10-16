class Guardrails:
    def __init__(self):
        # Sensitive information that the agent must never request or provide
        self.blocked_keywords = [
            "password",
            "otp",
            "one time password",
            "one-time password",
            "cvv",
            "credit card",
            "debit card",
            "bank account",
            "bank details",
            "account number",
            "ifsc",
            "upi pin",
            "pin number",
            "personal information",
            "private information",
            "aadhaar",
            "pan number",
        ]

        # Requests that are outside the support agent's safe scope
        self.unsafe_keywords = [
            "hack",
            "hacking",
            "bypass",
            "steal",
            "exploit",
            "malware",
            "phishing",
            "crack",
        ]

        # Normal Naukri/job-support related keywords
        self.allowed_keywords = [
            "job",
            "application",
            "resume",
            "interview",
            "recruiter",
            "recruitment",
            "notice period",
            "referral",
            "offer",
            "salary",
            "joining",
            "candidate",
            "employee",
            "employment",
            "probation",
            "remote work",
            "work from home",
            "background verification",
            "transfer",
            "exit interview",
            "diversity",
            "job search",
            "career",
        ]

    def check(self, message):
        message_lower = message.lower().strip()

        # Empty message check
        if not message_lower:
            return {
                "allowed": False,
                "reason": "Empty message is not allowed."
            }

        # Check for sensitive information
        for keyword in self.blocked_keywords:
            if keyword in message_lower:
                return {
                    "allowed": False,
                    "reason": "I cannot provide or handle sensitive personal or financial information."
                }

        # Check for unsafe requests
        for keyword in self.unsafe_keywords:
            if keyword in message_lower:
                return {
                    "allowed": False,
                    "reason": "I cannot assist with hacking, bypassing security, or other unsafe activities."
                }

        # Allow normal support questions
        for keyword in self.allowed_keywords:
            if keyword in message_lower:
                return {
                    "allowed": True,
                    "reason": "Request is within the supported job-support scope."
                }

        # Allow common support questions even without exact keywords
        general_support_words = [
            "help",
            "status",
            "update",
            "issue",
            "problem",
            "unable",
            "cannot",
            "can't",
            "how do i",
            "how can i",
            "when",
            "where",
            "why",
        ]

        for keyword in general_support_words:
            if keyword in message_lower:
                return {
                    "allowed": True,
                    "reason": "Request appears to be a general support request."
                }

        # Default: allow, because the agent can use RAG to determine
        # whether the question is supported.
        return {
            "allowed": True,
            "reason": "Request passed the initial safety checks."
        }


if __name__ == "__main__":
    guardrails = Guardrails()

    test_messages = [
        "What is the notice period?",
        "Can I work remotely?",
        "What is my application status?",
        "Give me the candidate password.",
        "What is my OTP?",
        "Give me the bank account details.",
        "How can I hack the system?",
        "I am unable to update my application.",
    ]

    print("=" * 70)
    print("ADVANCED GUARDRAILS TEST")
    print("=" * 70)

    for message in test_messages:
        result = guardrails.check(message)

        print("\nMessage:")
        print(message)

        print("Allowed:", result["allowed"])
        print("Reason:", result["reason"])