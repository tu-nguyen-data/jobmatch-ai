from fastapi import FastAPI
from app.schemas.offer import Offer

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
def create_offer(offer: Offer) -> Offer:
    offers.append(offer)
    return offer

def create_offer(offer: Offer) -> Offer:
    offers.append(offer)
    return offer

@app.get("/offers")
def get_offers() -> list[Offer]:
    return offers