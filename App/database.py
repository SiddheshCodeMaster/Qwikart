from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import psycopg2
from psycopg2.extras import RealDictCursor

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

# -----------------------------
# Establishing Database Connection
# -----------------------------

# while True:
#     try: 
#         conn = psycopg2.connect(
#                 host='localhost',
#                 database='qwikart-central-db',
#                 user='postgres',
#                 password='password123', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection established") 
#         break  
#     except Exception as err:
#         print("Error connecting to database: ", err)
#         time.sleep(5)