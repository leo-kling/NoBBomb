"""
This is an helper script aimed for contributors to test / analyse output for monitored services retrieval.
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi_app.routes import router
from services.core import NobbombCoreService

fast_api_app = FastAPI()
fast_api_app.state.nobbomb_core_service = NobbombCoreService()
fast_api_app.include_router(router=router)

client = TestClient(fast_api_app)


def test_nobbomb_anti_burst_service():
    """Test the NobbombAntiBurstService."""
    client.post("/nobbomb")
