from pydantic import BaseModel


class OfferCreate(BaseModel):
    title: str
    company: str
    location: str
    description: str


class Offer(OfferCreate):
    id: int