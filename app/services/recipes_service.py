from sqlalchemy.orm import Session
from app.models import RecipeModel, UserModel
from app.schemas import RecipeCreate, RecipeUpdate


def get_recipes_service(current_user: UserModel, db: Session) -> list[RecipeModel]:
    return db.query(RecipeModel).filter(RecipeModel.user_id == current_user.id).all()


def create_recipe_service(
    recipe_data: RecipeCreate, current_user: UserModel, db: Session
) -> RecipeModel:
    new_recipe = RecipeModel(
        title=recipe_data.title,
        content=recipe_data.content,
        prep_time=recipe_data.prep_time,
        user_id=current_user.id,
    )
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe


def update_recipe_service(
    update_data: RecipeUpdate, recipe: RecipeModel, db: Session
) -> RecipeModel:
    update_dict = update_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(recipe, key, value)

    db.commit()

    return recipe


def delete_recipe_service(recipe: RecipeModel, db: Session) -> None:
    db.delete(recipe)
    db.commit()
