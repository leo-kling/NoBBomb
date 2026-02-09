"""
This is an helper script aimed for contributors to test / analyse output for monitored services retrieval.
"""

import base64
import json

from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi_app.routes import router
from services.core import NobbombCoreService

fast_api_app = FastAPI()
fast_api_app.state.nobbomb_core_service = NobbombCoreService()
fast_api_app.include_router(router=router)

client = TestClient(fast_api_app)


def test_nobbomb_anti_burst_service():
    """Test the NoBBomb kill switch."""
    payload = {"costAmount": 100, "budgetAmount": 50}
    encoded = base64.b64encode(json.dumps(payload).encode("utf-8")).decode("ascii")
    client.post(
        "/kill_switch",
        json={"message": {"data": encoded}},
    )
