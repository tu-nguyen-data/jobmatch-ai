from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Bienvenue sur JobMatch AI",
        "status": "running",
    }

def test_create_offer():
    response = client.post(
        "/offers",
        json={
            "title": "Data Analyst Alternance",
            "company": "Airbus",
            "location": "Toulouse",
            "description": "Python, SQL et Power BI",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Data Analyst Alternance"
    assert data["company"] == "Airbus"
    assert data["location"] == "Toulouse"
    assert data["description"] == "Python, SQL et Power BI"
    assert isinstance(data["id"], int)

def test_create_and_get_offer():
    create_response = client.post(
        "/offers",
        json={
            "title": "Data Engineer Alternance",
            "company": "Capgemini",
            "location": "Toulouse",
            "description": "Python, SQL et pipelines de données",
        },
    )

    assert create_response.status_code == 200

    offer_id = create_response.json()["id"]

    get_response = client.get(f"/offers/{offer_id}")

    assert get_response.status_code == 200

    data = get_response.json()

    assert data["id"] == offer_id
    assert data["title"] == "Data Engineer Alternance"
    assert data["company"] == "Capgemini"