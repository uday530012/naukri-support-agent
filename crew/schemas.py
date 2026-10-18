from pydantic import BaseModel, Field


class NaukriSupportResponse(BaseModel):
    """
    Structured final response returned by the Naukri Support Crew.
    """

    status: str = Field(
        description="Response status, such as success or fallback."
    )

    response: str = Field(
        description="Final answer to the user's Naukri support question."
    )

    source: str = Field(
        description="Evidence source used for the response."
    )

    next_action: str = Field(
        description="Recommended next action for the user."
    )