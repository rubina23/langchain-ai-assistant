from pydantic import BaseModel, Field


class ChatResponse(BaseModel):
    answer: str = Field(description="The main answer to the user's question")
    summary: str = Field(description="A short summary of the answer")
    confidence: float = Field(
        description="Confidence score from 0 to 1"
    )
    category: str = Field(
        description="The category of the user's question"
    )
    keywords: list[str] = Field(
        description="Important keywords related to the question"
    )