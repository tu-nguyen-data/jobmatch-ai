from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.offer import Offer as OfferModel
from app.schemas.offer import Offer, OfferCreate

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