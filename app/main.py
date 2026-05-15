from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Quote Fetcher AI",
    description="Semantic book quote search powered by AI + Azure",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def home():
    return {"message": "Quote Fetcher AI is running 🚀"}