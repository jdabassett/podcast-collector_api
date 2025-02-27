from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = 'sqlite:///./pc.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
  db = SessionLocal()
  try:
      yield db
  finally:
      db.close()