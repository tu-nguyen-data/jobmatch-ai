import pandas as pd

from app.database import SessionLocal
from app.models.offer import Offer as OfferModel
from app.schemas.offer import OfferCreate


CSV_PATH = "data/offers_sample.csv"


def import_offers() -> None:
    df = pd.read_csv(CSV_PATH)

    db = SessionLocal()

    imported_count = 0
    skipped_count = 0

    try:
        for _, row in df.iterrows():
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
                print(
                    f"Déjà présente : "
                    f"{offer_data.title} - {offer_data.company}"
                )
                skipped_count += 1
                continue

            db_offer = OfferModel(**offer_data.model_dump())

            db.add(db_offer)
            imported_count += 1

        db.commit()

        print()
        print("Import terminé")
        print(f"Offres ajoutées : {imported_count}")
        print(f"Offres ignorées : {skipped_count}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    import_offers()