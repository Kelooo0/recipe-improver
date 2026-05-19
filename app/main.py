from fastapi import FastAPI

app = FastAPI()

@app.get('/', tags=["Health Check"])
def health_check():
    return {
        "status": "ok",
        "project": "Recipe Improver",
        "version": "1.0.0"
    }
