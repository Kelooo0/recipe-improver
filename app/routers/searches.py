from fastapi import APIRouter, Depends, status, Query
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import UserModel
from app.schemas import Search
from app.services.auth_service import get_current_user
from app.services.searches_service import get_searches_service, create_search_service

router = APIRouter()


@router.get("/")
def get_searches(
    current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)
) -> list[Search]:
    return get_searches_service(current_user, db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_search(
    ingredients: list[str] = Query(
        ...,
        min_length=1,
        max_length=20,
        description="Enter between 1 and 20 ingredients",
    ),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Search:
    return create_search_service(ingredients, current_user, db)
