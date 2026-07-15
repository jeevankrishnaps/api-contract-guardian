from fastapi import FastAPI
from app.routers import users

app=FastAPI(
    title="API Contract Guardian Demo",
    version="1.0.0",
    description="A demo API used to showcase automated contract-breakage detection",
)

app.include_router(users.router)


@app.get("/health")
def health():
    return {"status": "ok"}