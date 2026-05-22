from fastapi import FastAPI
from app.routers import auth, searches
from typing import Any

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(searches.router, prefix="/searches", tags=["Searches"])


@app.get("/", tags=["Health Check"])
def health_check() -> Any:
    return {"status": "ok", "project": "Recipe Improver", "version": "1.0.0"}
