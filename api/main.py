from fastapi import FastAPI
from api.routers.companies import router as companies_router
from api.routers.dashboard import router as dashboard_router

app = FastAPI(
    title="CareerLens-AI API",
    version="1.0.0",
    description="AI-Powered Job Market Intelligence Platform"
)

app.include_router(dashboard_router)
app.include_router(companies_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to CareerLens-AI API 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }