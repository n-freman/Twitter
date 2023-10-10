from fastapi import FastAPI

from ...bootstrap import bootstrap

bootstrap()

from .routers import auth, tweets

app = FastAPI(title="Twitter Clone API")

app.include_router(auth.router)
app.include_router(tweets.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
