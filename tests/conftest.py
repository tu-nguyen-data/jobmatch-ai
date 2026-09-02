import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.offer import Offer as OfferModel

from app.database import Base, DATABASE_URL
from app.main import app, get_db

# On utilise la même base PostgreSQL,
# mais uniquement le schéma réservé aux tests.
test_engine = create_engine(
    DATABASE_URL,
    connect_args={
        "options": "-csearch_path=jobmatch_test",
    },
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    # Nettoie le schéma de test avant les tests.
    Base.metadata.drop_all(bind=test_engine)

    # Crée les tables dans jobmatch_test.
    Base.metadata.create_all(bind=test_engine)

    yield

    # Nettoie après la session de tests.
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(autouse=True)
def clean_test_data():
    db = TestingSessionLocal()

    try:
        db.query(OfferModel).delete()
        db.commit()

        yield

        db.query(OfferModel).delete()
        db.commit()

    finally:
        db.close()