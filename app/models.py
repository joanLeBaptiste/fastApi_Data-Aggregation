from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# ✅ Table Angers Cadrillage (Zones)
class AngersCadrillage(Base):
    __tablename__ = "angers_cadrillage"

    id_zone = Column(String, primary_key=True)
    latitude_centre = Column(Float, nullable=False)
    longitude_centre = Column(Float, nullable=False)
    latitude_min = Column(Float, nullable=False)
    longitude_min = Column(Float, nullable=False)
    latitude_max = Column(Float, nullable=False)
    longitude_max = Column(Float, nullable=False)
    rayon_km = Column(Float, nullable=False)

    # Relation avec les chemins
    chemins = relationship("Chemin", back_populates="zone")


# ✅ Table Type Scores
class TypeScores(Base):
    __tablename__ = "type_scores"

    type_infra = Column(String, primary_key=True)
    score = Column(Integer, nullable=False)

    # Correction : "Infrastructures" au lieu de "Infrastructure"
    infrastructures = relationship("Infrastructures", back_populates="type_score")


# ✅ Table Infrastructures
class Infrastructures(Base):
    __tablename__ = "infrastructures"

    id_infra = Column(String, primary_key=True)
    nom = Column(String, nullable=False)
    type_infra = Column(String, ForeignKey("type_scores.type_infra"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Relation avec TypeScores
    type_score = relationship("TypeScores", back_populates="infrastructures")

    # Relation avec Chemins
    chemins = relationship("Chemin", back_populates="infrastructure")


# ✅ Table Chemins
class Chemin(Base):
    __tablename__ = "chemins"

    id_chemin = Column(String, primary_key=True)
    id_zone = Column(String, ForeignKey("angers_cadrillage.id_zone"), nullable=False)
    id_infra = Column(String, ForeignKey("infrastructures.id_infra"), nullable=False)
    type_infra = Column(String, nullable=False)
    distance_m = Column(Float, nullable=False)

    # Relations
    zone = relationship("AngersCadrillage", back_populates="chemins")
    infrastructure = relationship("Infrastructures", back_populates="chemins")
