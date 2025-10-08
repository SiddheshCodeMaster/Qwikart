from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

QWIKART_CENTRAL_DB_URL = 'postgresql://postgres:password123@localhost/qwikart-central-db'

engine = create_engine(QWIKART_CENTRAL_DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 