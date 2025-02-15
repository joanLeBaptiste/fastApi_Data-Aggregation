from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base  # Import de la base déclarative
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Création de l'engine de la base de données
engine = create_engine(settings.DATABASE_URL, echo=True)

# Définir Base qui sera utilisée par les modèles
Base = declarative_base()

# Session locale pour la base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dépendance pour récupérer une session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
