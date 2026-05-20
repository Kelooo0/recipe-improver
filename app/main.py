from fastapi import FastAPI
from app.routers import auth

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])


@app.get("/", tags=["Health Check"])
def health_check():
    return {"status": "ok", "project": "Recipe Improver", "version": "1.0.0"}
