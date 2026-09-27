from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.database import init_db

from app.routes.auth import router as auth_router
from app.routes.pages import router as page_router
from app.recommendations import (
    router as recommendation_router,
)


settings = get_settings()


app = FastAPI(

    title=settings.app_name,

    description=(
        "PocketSmart AI is a "
        "budget-aware AI planning "
        "assistant for home interiors, "
        "parties and jewelry."
    ),

    version="1.0.0",
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=(
        settings.cors_origin_list
    ),

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


app.mount(

    "/static",

    StaticFiles(
        directory="app/static"
    ),

    name="static",
)


app.include_router(
    auth_router
)

app.include_router(
    recommendation_router
)

app.include_router(
    page_router
)


@app.get("/api/health")
def health():

    return {
        "status": "ok",
        "service": settings.app_name,
    }


@app.on_event("startup")
def startup_event():

    Path("data").mkdir(
        exist_ok=True
    )

    init_db()