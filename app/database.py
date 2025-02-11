from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://suyashghimire:root@localhost:5432/local"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        print("Connection successful!")
        return True
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    test_connection() 