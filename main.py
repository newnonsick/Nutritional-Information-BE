from fastapi import FastAPI

from api.v1.routes import analyze
from core.middleware import add_middleware

app = FastAPI(
    title="Food Nutritional Information", version="1.0", docs_url="/documentation"
)

add_middleware(app)

app.include_router(analyze.router, prefix="/api/v1", tags=["Food Analysis"])


@app.get("/")
def root():
    return {"message": "Hello World!"}
