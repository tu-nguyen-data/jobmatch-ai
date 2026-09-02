import pytest
from sqlalchemy import create_engine, text
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
    with test_engine.connect() as connection:
        connection.execute(
            text(
                "CREATE SCHEMA IF NOT EXISTS "
                "jobmatch_test AUTHORIZATION jobmatch_user"
            )
        )
        connection.commit()

    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    yield

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