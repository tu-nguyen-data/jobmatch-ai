from pydantic import BaseModel


class Offer(BaseModel):
    title: str
    company: str
    location: str
    description: str