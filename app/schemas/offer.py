from pydantic import BaseModel, ConfigDict, Field


class OfferCreate(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    company: str = Field(min_length=2, max_length=255)
    location: str = Field(min_length=2, max_length=255)
    description: str = Field(min_length=10)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Data Analyst Alternance",
                "company": "Airbus",
                "location": "Toulouse",
                "description": "Python, SQL, Power BI et machine learning",
            }
        }
    )


class Offer(OfferCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)