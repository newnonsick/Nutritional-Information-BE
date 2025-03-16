from fastapi import Depends, FastAPI

from api.dependencies import get_current_user
from api.v1.routes import analyze, auth
from core.middleware import add_middleware

app = FastAPI(
    title="Food Nutritional Information",
    version="1.0",
    docs_url="/documentation",
)

add_middleware(app)

app.include_router(
    analyze.router,
    prefix="/api/v1",
    tags=["Food Analysis"],
)
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])


@app.get("/health", tags=["Health Check"])
def health():
    return {"status": "UP"}
