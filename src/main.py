from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles

from src.api import router
from src.core.config import settings
from src.core.lifespan import lifespan

app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    title="Authorization API template",
)

app.mount(
    "/static",
    StaticFiles(
        directory=settings.upload_dir,
    ),
    name="static",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
        # "http://prod-team-16-qi3lk0el.REDACTED",
        # "localhost",
        # "http://localhost",
        # "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
