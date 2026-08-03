from fastapi import FastAPI

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