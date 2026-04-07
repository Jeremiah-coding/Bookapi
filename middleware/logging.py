import logging
import time
import uuid

from fastapi import Request
from fastapi.responses import Response

logger = logging.getLogger("bookapi")
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


async def logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    try:
        response = await call_next(request)
    except Exception as exc:
        duration = time.perf_counter() - start_time
        logger.error(
            "Unhandled error | request_id=%s method=%s path=%s duration=%.4fs error=%s",
            request_id,
            request.method,
            request.url.path,
            duration,
            repr(exc),
        )
        raise

    duration = time.perf_counter() - start_time

    logger.info(
        "method=%s path=%s status=%d duration=%.4fs request_id=%s",
        request.method,
        request.url.path,
        response.status_code,
        duration,
        request_id,
    )

    response.headers["X-Process-Time"] = f"{duration:.4f}"
    response.headers["X-Request-ID"] = request_id

    return response