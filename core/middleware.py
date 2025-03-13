import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request
from core.logging import logger
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        logger.info(f"Incoming request: {request.method} {request.url.path}")
        logger.debug(f"Request headers: {dict(request.headers)}")

        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            response = JSONResponse(
                status_code=500, content={"detail": "Internal Server Error"}
            )

        process_time = time.time() - start_time

        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Request processed in: {process_time:.4f} seconds")

        response.headers["X-Processing-Time"] = str(process_time)
        response.headers["X-Custom-Header"] = "MyCustomValue"

        return response


def add_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(CustomMiddleware)
