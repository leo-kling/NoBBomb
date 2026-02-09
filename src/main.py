"""Run Uvicorn + Fast API app."""

import uvicorn

from fastapi_app.fast_api import fast_api_app
from helpers.constants import APP_CONFIG, APP_LOGGER, DEBUG_MODE

APP_LOGGER.info(msg=f"App configuration: {APP_CONFIG}")
if DEBUG_MODE:
    APP_LOGGER.warning(msg="Running in DEBUG MODE - Verbose logging enabled.")
    log_level = "debug"
else:
    log_level = "info"

uvicorn.run(app=fast_api_app, host="0.0.0.0", port=8080, log_level=log_level)
