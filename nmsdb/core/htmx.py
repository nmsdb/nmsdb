from fastapi import FastAPI, Request
from structlog import get_logger

logger = get_logger("nmsdb.core.htmx")


def is_htmx(request: Request):
    if request.headers.get("HX-Request") == "true":
        logger.debug(f"htmx call: {request.url.path}")
        return True
