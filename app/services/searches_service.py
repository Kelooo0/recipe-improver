from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models import SearchModel, UserModel
from app.config import settings


def validate_ingredients(ingredients: list[str]) -> str:
    ingredients_clean = []
    for i in ingredients:
        i = i.strip().lower()
        if not i:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ingredient name can't be empty",
            )
        if i in settings.BANNED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{i}, is not a valid ingredient",
            )
        if len(i) < 3 or len(i) > 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ingredient name must contain between 3 and 50 characters",
            )
        ingredients_clean.append(i)
    return ", ".join(ingredients_clean)


def get_searches_service(current_user: UserModel, db: Session) -> list[SearchModel]:
    return db.query(SearchModel).filter(SearchModel.user_id == current_user.id).all()


def create_search_service(
    ingredients: list[str], current_user: UserModel, db: Session
) -> SearchModel:
    ingredients_str = validate_ingredients(ingredients)
    new_search = SearchModel(ingredients=ingredients_str, user_id=current_user.id)
    db.add(new_search)
    db.commit()
    db.refresh(new_search)
    return new_search
