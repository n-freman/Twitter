from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from twitter import config
from twitter.bootstrap import bootstrap

bootstrap()

from .routers import auth, tweets

app = FastAPI(title="Twitter Clone API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(tweets.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}

