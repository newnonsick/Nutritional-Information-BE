from fastapi import FastAPI

from api.v1.routes import analyze, auth, meals, user
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
app.include_router(user.router, prefix="/api/v1", tags=["User"])
app.include_router(
    meals.router,
    prefix="/api/v1",
    tags=["Meal"],
)


@app.get("/health", tags=["Health Check"])
def health():
    return {"status": "UP"}
