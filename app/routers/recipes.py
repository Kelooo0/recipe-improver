from fastapi import APIRouter, Depends, status, HTTPException
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import UserModel
from app.services.auth_service import get_current_user
from app.services.recipes_service import (
    get_recipes_service,
    create_recipe_service,
    update_recipe_service,
    delete_recipe_service,
)
from app.schemas import Recipe, RecipeCreate, RecipeUpdate
from app.models import RecipeModel

router = APIRouter()


def validate_recipe(
    id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> RecipeModel:
    recipe = (
        db.query(RecipeModel)
        .filter(RecipeModel.id == id, RecipeModel.user_id == current_user.id)
        .first()
    )
    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found"
        )
    return recipe


@router.get("/")
def get_recipes(
    current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)
) -> list[Recipe]:
    return get_recipes_service(current_user, db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_recipe(
    recipe_data: RecipeCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Recipe:
    return create_recipe_service(recipe_data, current_user, db)


@router.patch("/{id}")
def update_recipe(
    update_data: RecipeUpdate,
    recipe: RecipeModel = Depends(validate_recipe),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Recipe:
    return update_recipe_service(update_data, recipe, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(
    recipe: RecipeModel = Depends(validate_recipe),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    return delete_recipe_service(recipe, db)
