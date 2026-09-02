from io import BytesIO

import pandas as pd
from fastapi import Depends, FastAPI, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.offer import Offer as OfferModel
from app.schemas.offer import Offer, OfferCreate
from app.services.offer_import import import_offers_dataframe

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

from fastapi import FastAPI, HTTPException

from app.schemas.offer import Offer, OfferCreate

app = FastAPI(
    title="JobMatch AI API",
    description="API de recommandation d'offres d'alternance.",
    version="0.1.0",
)


@app.get("/")
def read_root() -> dict[str, str]:
    """Retourne un message lorsque l'API fonctionne."""
    return {
        "message": "Bienvenue sur JobMatch AI",
        "status": "running",
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    """Vérifie que l'API est disponible."""
    return {"status": "ok"}

@app.post("/offers")
def create_offer(
    offer_data: OfferCreate,
    db: Session = Depends(get_db),
) -> Offer:
    db_offer = OfferModel(**offer_data.model_dump())

    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)

    return db_offer

def create_offer(offer: Offer) -> Offer:
    offers.append(offer)
    return offer

@app.get("/offers")
def get_offers(
    db: Session = Depends(get_db),
) -> list[Offer]:
    return db.query(OfferModel).all()

@app.get("/offers/{offer_id}")
def get_offer(
    offer_id: int,
    db: Session = Depends(get_db),
) -> Offer:
    offer = db.get(OfferModel, offer_id)

    if offer is None:
        raise HTTPException(
            status_code=404,
            detail="Offre introuvable",
        )

    return offer

@app.delete("/offers/{offer_id}")
def delete_offer(
    offer_id: int,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    offer = db.get(OfferModel, offer_id)

    if offer is None:
        raise HTTPException(
            status_code=404,
            detail="Offre introuvable",
        )

    db.delete(offer)
    db.commit()

    return {"message": "Offre supprimée"}

@app.put("/offers/{offer_id}")
def update_offer(
    offer_id: int,
    offer_data: OfferCreate,
    db: Session = Depends(get_db),
) -> Offer:
    offer = db.get(OfferModel, offer_id)

    if offer is None:
        raise HTTPException(
            status_code=404,
            detail="Offre introuvable",
        )

    offer.title = offer_data.title
    offer.company = offer_data.company
    offer.location = offer_data.location
    offer.description = offer_data.description

    db.commit()
    db.refresh(offer)

    return offer

@app.post("/offers/import")
async def import_offers_csv(
    file: UploadFile,
    db: Session = Depends(get_db),
) -> dict:
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Le fichier doit être au format CSV",
        )

    content = await file.read()

    try:
        df = pd.read_csv(BytesIO(content))
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Impossible de lire le fichier CSV",
        )

    required_columns = {
        "title",
        "company",
        "location",
        "description",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise HTTPException(
            status_code=400,
            detail=f"Colonnes manquantes : {', '.join(missing_columns)}",
        )

    return import_offers_dataframe(df, db)