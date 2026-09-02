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

def test_update_offer():
    create_response = client.post(
        "/offers",
        json={
            "title": "Data Analyst Alternance",
            "company": "Airbus",
            "location": "Toulouse",
            "description": "Python, SQL et Power BI",
        },
    )

    offer_id = create_response.json()["id"]

    update_response = client.put(
        f"/offers/{offer_id}",
        json={
            "title": "Data Analyst Alternance - Updated",
            "company": "Airbus",
            "location": "Toulouse",
            "description": "Python, SQL, Power BI et machine learning",
        },
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["id"] == offer_id
    assert data["title"] == "Data Analyst Alternance - Updated"
    assert data["description"] == (
        "Python, SQL, Power BI et machine learning"
    )


def test_delete_offer():
    create_response = client.post(
        "/offers",
        json={
            "title": "BI Analyst Alternance",
            "company": "Sopra Steria",
            "location": "Toulouse",
            "description": "Power BI, SQL, Excel et reporting",
        },
    )

    offer_id = create_response.json()["id"]

    delete_response = client.delete(f"/offers/{offer_id}")

    assert delete_response.status_code == 200
    assert delete_response.json() == {
        "message": "Offre supprimée"
    }

    get_response = client.get(f"/offers/{offer_id}")

    assert get_response.status_code == 404
    assert get_response.json() == {
        "detail": "Offre introuvable"
    }