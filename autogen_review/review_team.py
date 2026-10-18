import asyncio

from autogen_agentchat.teams import RoundRobinGroupChat

from autogen_review.review_agents import (
    reviewer_agent,
    final_editor_agent,
    ReviewMessage,
    FinalEditorMessage,
)


# ============================================================
# AUTOGEN ROUND-ROBIN REVIEW TEAM
# ============================================================

review_team = RoundRobinGroupChat(
    participants=[
        reviewer_agent,
        final_editor_agent,
    ],
    max_turns=2,
    custom_message_types=[
        ReviewMessage,
        FinalEditorMessage,
    ],
)


# ============================================================
# TEST CREWAI DRAFT
# ============================================================

task = """
Review the following CrewAI draft response.

USER QUESTION:
What is the notice period policy?

EVIDENCE:
The Naukri knowledge base states that the standard notice
period is 30 days.

CREWAI DRAFT:
The standard notice period is 60 days.

The reviewer must check the draft against the evidence.

The Final Editor must revise the response if the draft contains
an unsupported claim.

Return the final structured response.
"""


# ============================================================
# RUN REVIEW
# ============================================================

async def main():

    print("=" * 70)
    print("AUTOGEN ROUND-ROBIN REVIEW")
    print("=" * 70)

    result = await review_team.run(
        task=task
    )

    print("\n" + "=" * 70)
    print("AUTOGEN REVIEW COMPLETED")
    print("=" * 70)

    for message in result.messages:

        print(f"\nAgent: {message.source}")
        print(f"Message: {message.to_text()}")

    print("\n" + "=" * 70)
    print("STOP REASON")
    print("=" * 70)

    print(result.stop_reason)


if __name__ == "__main__":
    asyncio.run(main())