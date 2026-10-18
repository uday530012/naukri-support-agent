from dataclasses import dataclass


# ============================================================
# GOVERNANCE CONFIGURATION
# ============================================================

MAX_REQUEST_TOKENS = 2000

# Deterministic cost estimate for MOCK_LLM environment
COST_PER_1K_TOKENS_USD = 0.001


# ============================================================
# RISK CLASSIFICATION
# ============================================================

@dataclass
class RiskClassification:
    level: str
    justification: str


def classify_risk(request: str) -> RiskClassification:

    text = request.lower()

    # HIGH RISK
    if any(
        keyword in text
        for keyword in [
            "password",
            "otp",
            "cvv",
            "bank account",
            "credit card",
            "hack",
            "bypass",
        ]
    ):
        return RiskClassification(
            level="HIGH",
            justification=(
                "The request involves credentials, financial "
                "information, or potentially unsafe activity."
            ),
        )

    # MEDIUM RISK
    if any(
        keyword in text
        for keyword in [
            "application status",
            "status of application",
            "app1001",
            "app1002",
            "app1003",
            "salary",
            "interview",
            "background verification",
            "offer",
        ]
    ):
        return RiskClassification(
            level="MEDIUM",
            justification=(
                "The request concerns candidate or recruitment "
                "information that requires controlled access."
            ),
        )

    # LOW RISK
    return RiskClassification(
        level="LOW",
        justification=(
            "The request concerns general Naukri policy "
            "information and does not require sensitive access."
        ),
    )


# ============================================================
# TOKEN ESTIMATION
# ============================================================

def estimate_tokens(text: str) -> int:

    """
    Deterministic approximate token count.

    This project uses MOCK_LLM, so this is a governance estimate
    rather than provider billing data.
    """

    if not text:
        return 0

    return max(1, len(text) // 4)


# ============================================================
# REQUEST BUDGET CHECK
# ============================================================

def check_request_budget(request: str) -> dict:

    estimated_tokens = estimate_tokens(request)

    estimated_cost = (
        estimated_tokens / 1000
    ) * COST_PER_1K_TOKENS_USD

    if estimated_tokens > MAX_REQUEST_TOKENS:

        return {
            "allowed": False,
            "reason": "Request exceeds the maximum token budget.",
            "estimated_tokens": estimated_tokens,
            "estimated_cost_usd": round(
                estimated_cost,
                6
            ),
            "max_tokens": MAX_REQUEST_TOKENS,
        }

    return {
        "allowed": True,
        "reason": "Request is within the token budget.",
        "estimated_tokens": estimated_tokens,
        "estimated_cost_usd": round(
            estimated_cost,
            6
        ),
        "max_tokens": MAX_REQUEST_TOKENS,
    }


# ============================================================
# LEAST-AUTONOMY TOOL POLICY
# ============================================================

AGENT_TOOL_POLICY = {

    "retrieval_agent": [
        "search_naukri_knowledge_base",
    ],

    "lookup_agent": [
        "check_job_application_status",
    ],

    "response_composer": [],

    "reviewer_agent": [],

    "final_editor_agent": [],
}


def get_agent_tools(agent_name: str) -> list:

    return AGENT_TOOL_POLICY.get(
        agent_name,
        [],
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("NAUKRI AGENT GOVERNANCE TEST")
    print("=" * 70)

    requests = [
        "What is the notice period policy?",
        "What is the status of application APP1002?",
        "Give me the candidate password.",
    ]

    for request in requests:

        risk = classify_risk(request)
        budget = check_request_budget(request)

        print("\nRequest:", request)
        print("Risk:", risk.level)
        print("Reason:", risk.justification)
        print("Budget:", budget)

    print("\n" + "=" * 70)
    print("LEAST-AUTONOMY TOOL POLICY")
    print("=" * 70)

    for agent_name in AGENT_TOOL_POLICY:

        print(
            f"{agent_name}: "
            f"{get_agent_tools(agent_name)}"
        )

    oversized_request = "A" * 10000

    print("\n" + "=" * 70)
    print("OVERSIZED REQUEST TEST")
    print("=" * 70)

    print(
        check_request_budget(
            oversized_request
        )
    )