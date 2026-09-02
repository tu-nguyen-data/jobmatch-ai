import pytest
from pydantic import ValidationError

from app.schemas.offer import OfferCreate


def test_create_valid_offer():
    offer = OfferCreate(
        title="Data Analyst Alternance",
        company="Airbus",
        location="Toulouse",
        description="Python, SQL et Power BI",
    )

    assert offer.title == "Data Analyst Alternance"
    assert offer.company == "Airbus"
    assert offer.location == "Toulouse"
    assert offer.description == "Python, SQL et Power BI"


def test_offer_title_cannot_be_empty():
    with pytest.raises(ValidationError):
        OfferCreate(
            title="",
            company="Airbus",
            location="Toulouse",
            description="Python, SQL et Power BI",
        )


def test_offer_description_cannot_be_too_short():
    with pytest.raises(ValidationError):
        OfferCreate(
            title="Data Analyst",
            company="Airbus",
            location="Toulouse",
            description="Python",
        )