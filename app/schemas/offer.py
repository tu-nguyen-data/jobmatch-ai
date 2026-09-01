from pydantic import BaseModel, ConfigDict


class OfferCreate(BaseModel):
    title: str
    company: str
    location: str
    description: str


class Offer(OfferCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)