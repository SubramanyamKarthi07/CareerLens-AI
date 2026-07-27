from fastapi import FastAPI
from api.routers.companies import router as companies_router
from api.routers.dashboard import router as dashboard_router
from api.routers.locations import router as locations_router
from api.routers.sources import router as sources_router
from api.routers.trends import router as trends_router
from api.routers.jobs import router as jobs_router


app = FastAPI(
    title="CareerLens-AI API",
    version="1.0.0",
    description="AI-Powered Job Market Intelligence Platform"
)

app.include_router(dashboard_router)
app.include_router(companies_router)
app.include_router(locations_router)
app.include_router(sources_router)
app.include_router(trends_router)
app.include_router(jobs_router)

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