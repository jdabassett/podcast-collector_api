from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import Session, sessionmaker
from typing import Generator

from ..main import app, Base
from ..database import get_db
from .. import models

client = TestClient(app)

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread":False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
  db = TestingSessionLocal()
  try:
    yield db
  finally:
    db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def session() -> Generator[Session, None, None]:
  Base.metadata.create_all(bind=engine)
  
  db_session = TestingSessionLocal()

  # add user to temporary testing database
  db_user = models.User(name="testing_name", email="testing_email",password="testing_password")
  db_session.add(db_user)
  db_session.commit()
  db_session.refresh(db_user)

  yield db_session

  db_session.close()
  Base.metadata.drop_all(bind=engine)


def test_get_user():
  assert True == True




