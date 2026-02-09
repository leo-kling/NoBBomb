"""Main FAST API routes config file."""

from typing import Any

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse

from helpers.constants import APP_LOGGER
from services.core import NobbombCoreService

router = APIRouter()


def get_start_app_objects(request: Request) -> dict[str, Any]:
    """Return all start app objects.

    Use it as **kwargs -> **start_app_objects"""
    return {
        "nobbomb_core_service": request.app.state.nobbomb_core_service,
    }


@router.get(path="/favicon.ico")
def favicon() -> Response:
    """Basic route to ignore favicon.ico call."""
    return Response(status_code=204)


@router.post(path="/nobbomb")
def nobbomb(
    start_app_objects: dict[str, Any] = Depends(dependency=get_start_app_objects),
) -> JSONResponse:
    """Run Nobbomb checks."""
    nobbomb_core_service: NobbombCoreService = start_app_objects["nobbomb_core_service"]
    data = nobbomb_core_service.experimental_anti_burst()
    return JSONResponse(content=data)


@router.post(path="/kill_switch")
async def kill_switch(
    request: Request,
    start_app_objects: dict[str, Any] = Depends(dependency=get_start_app_objects),
) -> Response:
    """Run Kill Switch Only."""
    nobbomb_core_service: NobbombCoreService = start_app_objects["nobbomb_core_service"]

    is_budget_alert_triggered = await nobbomb_core_service.check_budget_alert_status(
        request_from_event_arc=request
    )

    if not is_budget_alert_triggered:
        APP_LOGGER.info(msg="Budget Alert not reached. Kill switch not triggered.")
    else:
        APP_LOGGER.critical(msg="Kill switch triggered. Budget Alert reached.")
        nobbomb_core_service.kill_switch_service.activate()
    return Response(status_code=200)
