from pydantic import BaseModel, Field
from typing import Literal
from model.model import model

class ReviewResult(BaseModel):

    decision: Literal[
        "APPROVE",
        "REVISE"
    ] = Field(
        description="Whether the work should be approved or revised."
    )

    feedback: str = Field(
        description="Detailed review feedback."
    )


review_model = model.with_structured_output(
    ReviewResult
)