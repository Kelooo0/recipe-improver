from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str


class RecipeBase(BaseModel):
    title: str = Field(..., max_length=100)
    content: str
    prep_time: int | None = None


class RecipeCreate(RecipeBase):
    pass


class RecipeList(BaseModel):
    recipes: list[RecipeCreate]


class RecipeUpdate(RecipeBase):
    title: str | None = Field(None, max_length=100)
    content: str | None = None
    prep_time: int | None = None


class Recipe(RecipeBase):
    id: int
    user_id: int
    search_id: int | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Search(BaseModel):
    id: int
    user_id: int
    ingredients: str
    created_at: datetime
    search_recipes: list[Recipe] | None

    model_config = ConfigDict(from_attributes=True)
