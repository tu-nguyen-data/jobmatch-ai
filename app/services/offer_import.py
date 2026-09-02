import pandas as pd
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.models.offer import Offer as OfferModel
from app.schemas.offer import OfferCreate


def import_offers_dataframe(
    df: pd.DataFrame,
    db: Session,
) -> dict:
    imported_count = 0
    skipped_count = 0
    invalid_count = 0
    errors = []

    for index, row in df.iterrows():
        try:
            offer_data = OfferCreate(
                title=row["title"],
                company=row["company"],
                location=row["location"],
                description=row["description"],
            )

            existing_offer = (
                db.query(OfferModel)
                .filter(
                    OfferModel.title == offer_data.title,
                    OfferModel.company == offer_data.company,
                    OfferModel.location == offer_data.location,
                )
                .first()
            )

            if existing_offer:
                skipped_count += 1
                continue

            db_offer = OfferModel(**offer_data.model_dump())

            db.add(db_offer)
            db.commit()

            imported_count += 1

        except ValidationError as error:
            db.rollback()
            invalid_count += 1

            errors.append(
                {
                    "line": index + 2,
                    "errors": [
                        {
                            "field": validation_error["loc"][0],
                            "message": validation_error["msg"],
                        }
                        for validation_error in error.errors()
                    ],
                }
            )

    return {
        "message": "Import terminé",
        "imported": imported_count,
        "duplicates": skipped_count,
        "invalid": invalid_count,
        "errors": errors,
    }