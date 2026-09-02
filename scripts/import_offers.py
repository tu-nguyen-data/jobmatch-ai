import pandas as pd
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.database import SessionLocal
from app.models.offer import Offer as OfferModel
from app.schemas.offer import OfferCreate


CSV_PATH = "data/offers_sample.csv"


def import_offers() -> None:
    df = pd.read_csv(CSV_PATH)

    db = SessionLocal()

    imported_count = 0
    skipped_count = 0
    invalid_count = 0

    try:
        for index, row in df.iterrows():
            try:
                # 1. Validation des données avec Pydantic
                offer_data = OfferCreate(
                    title=row["title"],
                    company=row["company"],
                    location=row["location"],
                    description=row["description"],
                )

                # 2. Vérification des doublons
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
                        f"Ligne {index + 2} ignorée : "
                        f"{offer_data.title} - {offer_data.company} "
                        f"déjà présente"
                    )
                    skipped_count += 1
                    continue

                # 3. Création de l'offre
                db_offer = OfferModel(**offer_data.model_dump())

                db.add(db_offer)
                db.commit()

                imported_count += 1

                print(
                    f"Ligne {index + 2} importée : "
                    f"{offer_data.title} - {offer_data.company}"
                )

            except ValidationError as error:
                db.rollback()
                invalid_count += 1

                print()
                print(f"Ligne {index + 2} invalide :")

                for validation_error in error.errors():
                    field = validation_error["loc"][0]
                    message = validation_error["msg"]

                    print(f"  - {field}: {message}")

            except SQLAlchemyError as error:
                db.rollback()
                invalid_count += 1

                print()
                print(f"Erreur PostgreSQL à la ligne {index + 2}:")
                print(f"  {error}")

        print()
        print("===== Résumé de l'import =====")
        print(f"Offres ajoutées  : {imported_count}")
        print(f"Doublons ignorés : {skipped_count}")
        print(f"Lignes invalides : {invalid_count}")

    finally:
        db.close()


if __name__ == "__main__":
    import_offers()