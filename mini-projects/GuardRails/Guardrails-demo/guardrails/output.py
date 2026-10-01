from pydantic import BaseModel, Field


class AgentResponse(BaseModel):

    answer: str = Field(
        min_length=1
    )

    confidence: float = Field(
        ge=0,
        le=1
    )


def validate_output(
    output: dict
) -> AgentResponse:

    return AgentResponse.model_validate(
        output
    )