from app.database import Base
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)

    recipes = relationship("RecipeModel", back_populates="owner")
    searches = relationship("SearchModel", back_populates="creator")


class RecipeModel(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    prep_time = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    search_id = Column(Integer, ForeignKey("searches.id"), nullable=False)

    owner = relationship("UserModel", back_populates="recipes")
    search = relationship("SearchModel", back_populates="search_recipes")


class SearchModel(Base):
    __tablename__ = "searches"

    id = Column(Integer, primary_key=True, index=True)
    ingredients = Column(String(100), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    search_recipes = relationship("RecipeModel", back_populates="search")
    creator = relationship("UserModel", back_populates="searches")
