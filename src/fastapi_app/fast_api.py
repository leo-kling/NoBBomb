"""Fast API main app."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi_app.routes import router
from services.core import NobbombCoreService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Global Contexte Instances."""
    app.state.nobbomb_core_service = NobbombCoreService()
    yield


fast_api_app = FastAPI(lifespan=lifespan)
fast_api_app.include_router(router=router)
