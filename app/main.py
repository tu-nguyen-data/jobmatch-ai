from fastapi import FastAPI, HTTPException

from app.schemas.offer import Offer, OfferCreate

app = FastAPI(
    title="JobMatch AI API",
    description="API de recommandation d'offres d'alternance.",
    version="0.1.0",
)

offers: list[Offer] = []

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
def create_offer(offer_data: OfferCreate) -> Offer:
    offer = Offer(
        id=len(offers) + 1,
        **offer_data.model_dump(),
    )

    offers.append(offer)

    return offer

def create_offer(offer: Offer) -> Offer:
    offers.append(offer)
    return offer

@app.get("/offers")
def get_offers() -> list[Offer]:
    return offers

@app.get("/offers/{offer_id}")
def get_offer(offer_id: int) -> Offer:
    for offer in offers:
        if offer.id == offer_id:
            return offer

    raise HTTPException(
        status_code=404,
        detail="Offre introuvable",
    )