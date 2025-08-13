from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorites=relationship("Favorites", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
            "username": self.username,
            "is_active": self.is_active,
        }

class Personaje(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(60), nullable=False)
    gender:Mapped[str] = mapped_column(String(10), nullable=False) 
    favoritesP=relationship("Favorites", back_populates="personaje")

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
        }
        
class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(60), nullable=False)
    climate:Mapped[str] = mapped_column(String(20), nullable=False)
    planetsFav=relationship("Favorites", back_populates="planet")


    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
        }

class Favorites(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user=relationship("User", back_populates="favorites")
    personajeid:Mapped[int] = mapped_column(ForeignKey("personaje.id"), nullable=True)
    personaje=relationship("Personaje", back_populates="favoritesP")
    planetid:Mapped[int] = mapped_column(ForeignKey("planet.id"),nullable=True)
    planet=relationship("Planet", back_populates="planetsFav")

    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "personajeid": self.personajeid,
            "planetid": self.planetid,
        }