from fastapi import FastAPI

from ...bootstrap import bootstrap
from .routers import auth

bootstrap()

app = FastAPI(title="Twitter Clone API")

app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
