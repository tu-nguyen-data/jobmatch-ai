from pydantic import BaseModel, Field


class MatchRequest(BaseModel):
    candidate_text: str = Field(min_length=10)

class MatchResult(BaseModel):
    offer_id: int
    title: str
    company: str
    location: str
    score: float