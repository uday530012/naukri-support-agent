from typing import Any, Mapping, Sequence

from pydantic import BaseModel, Field

from autogen_agentchat.agents import BaseChatAgent
from autogen_agentchat.base import Response
from autogen_agentchat.messages import (
    BaseChatMessage,
    StructuredMessage,
)
from autogen_core import CancellationToken


# ============================================================
# PYDANTIC STRUCTURED OUTPUT
# ============================================================

class ReviewOutput(BaseModel):
    decision: str = Field(
        description="APPROVE or REVISE"
    )
    issue: str = Field(
        description="Grounding issue found by the reviewer"
    )
    recommendation: str = Field(
        description="Recommended correction"
    )


class FinalEditorOutput(BaseModel):
    decision: str = Field(
        description="APPROVED or REVISED"
    )
    final_response: str = Field(
        description="Final grounded Naukri support response"
    )
    source: str = Field(
        description="Evidence source"
    )


# ============================================================
# CUSTOM AUTOGEN MESSAGE TYPES
# ============================================================

class ReviewMessage(StructuredMessage[ReviewOutput]):
    pass


class FinalEditorMessage(StructuredMessage[FinalEditorOutput]):
    pass


# ============================================================
# REVIEWER AGENT
# ============================================================

class NaukriReviewerAgent(BaseChatAgent):

    def __init__(self):
        super().__init__(
            name="naukri_reviewer",
            description=(
                "Reviews CrewAI support drafts for grounding "
                "against supplied Naukri evidence."
            ),
        )

    @property
    def produced_message_types(
        self,
    ) -> Sequence[type[BaseChatMessage]]:
        return (ReviewMessage,)

    async def on_messages(
        self,
        messages: Sequence[BaseChatMessage],
        cancellation_token: CancellationToken,
    ) -> Response:

        text = "\n".join(
            message.to_text()
            for message in messages
        )

        # Deliberate grounding test.
        # The supplied evidence says notice period is 30 days,
        # while the draft below deliberately claims 60 days.
        if "60 days" in text.lower():

            result = ReviewOutput(
                decision="REVISE",
                issue=(
                    "The draft claims a 60-day notice period, "
                    "but the supplied evidence supports a "
                    "30-day notice period."
                ),
                recommendation=(
                    "Remove the unsupported 60-day claim and "
                    "use only the 30-day notice period supported "
                    "by the evidence."
                ),
            )

        else:

            result = ReviewOutput(
                decision="APPROVE",
                issue="No unsupported claim detected.",
                recommendation=(
                    "Approve the response without changes."
                ),
            )

        message = ReviewMessage(
            content=result,
            source=self.name,
        )

        return Response(chat_message=message)

    async def on_reset(
        self,
        cancellation_token: CancellationToken,
    ) -> None:
        pass

    async def on_pause(
        self,
        cancellation_token: CancellationToken,
    ) -> None:
        pass

    async def on_resume(
        self,
        cancellation_token: CancellationToken,
    ) -> None:
        pass

    async def save_state(self) -> Mapping[str, Any]:
        return {}

    async def load_state(
        self,
        state: Mapping[str, Any],
    ) -> None:
        pass

    async def close(self) -> None:
        pass


# ============================================================
# FINAL EDITOR AGENT
# ============================================================

class NaukriFinalEditorAgent(BaseChatAgent):

    def __init__(self):
        super().__init__(
            name="naukri_final_editor",
            description=(
                "Produces the final grounded Naukri support "
                "response after reviewing the CrewAI draft."
            ),
        )

    @property
    def produced_message_types(
        self,
    ) -> Sequence[type[BaseChatMessage]]:
        return (FinalEditorMessage,)

    async def on_messages(
        self,
        messages: Sequence[BaseChatMessage],
        cancellation_token: CancellationToken,
    ) -> Response:

        text = "\n".join(
            message.to_text()
            for message in messages
        )

        if "60 days" in text.lower():

            final_response = (
                "The notice period policy states that the "
                "standard notice period is 30 days."
            )

            result = FinalEditorOutput(
                decision="REVISED",
                final_response=final_response,
                source="Naukri Knowledge Base",
            )

        else:

            result = FinalEditorOutput(
                decision="APPROVED",
                final_response=(
                    "The response is supported by the "
                    "available Naukri evidence."
                ),
                source="Naukri Knowledge Base",
            )

        message = FinalEditorMessage(
            content=result,
            source=self.name,
        )

        return Response(chat_message=message)

    async def on_reset(
        self,
        cancellation_token: CancellationToken,
    ) -> None:
        pass

    async def on_pause(
        self,
        cancellation_token: CancellationToken,
    ) -> None:
        pass

    async def on_resume(
        self,
        cancellation_token: CancellationToken,
    ) -> None:
        pass

    async def save_state(self) -> Mapping[str, Any]:
        return {}

    async def load_state(
        self,
        state: Mapping[str, Any],
    ) -> None:
        pass

    async def close(self) -> None:
        pass


# ============================================================
# CREATE TWO REVIEW AGENTS
# ============================================================

reviewer_agent = NaukriReviewerAgent()
final_editor_agent = NaukriFinalEditorAgent()