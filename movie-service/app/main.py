from fastapi import FastAPI
from app.api.movies import movies
from app.api.database import engine
from app.api import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_url="/api/v1/movies/openapi.json", docs_url="/api/v1/movies/docs")

app.include_router(movies, prefix='/api/v1/movies', tags=['movies'])
