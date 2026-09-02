import pandas as pd

from app.database import SessionLocal
from app.services.offer_import import import_offers_dataframe


CSV_PATH = "data/offers_sample.csv"


def import_offers() -> None:
    df = pd.read_csv(CSV_PATH)

    db = SessionLocal()

    try:
        result = import_offers_dataframe(df, db)

        print()
        print("===== Résumé de l'import =====")
        print(f"Offres ajoutées  : {result['imported']}")
        print(f"Doublons ignorés : {result['duplicates']}")
        print(f"Lignes invalides : {result['invalid']}")

        if result["errors"]:
            print()
            print("Erreurs détectées :")

            for error in result["errors"]:
                print(f"Ligne {error['line']} :")

                for detail in error["errors"]:
                    print(
                        f"  - {detail['field']}: "
                        f"{detail['message']}"
                    )

    finally:
        db.close()


if __name__ == "__main__":
    import_offers()