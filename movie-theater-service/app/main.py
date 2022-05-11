from fastapi import FastAPI
from app.api.movie_theaters.movies_theaters import moviesTheaters
from app.api.in_theaters.in_theaters import inTheaters
from app.api.database import engine
from app.api.in_theaters import models as models_in_theaters
from app.api.movie_theaters import models as models_movie_theaters

models_in_theaters.Base.metadata.create_all(bind=engine)
models_movie_theaters.Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_url="/api/v1/movies-theater/openapi.json", docs_url="/api/v1/movies-theater/docs")

app.include_router(moviesTheaters, prefix='/api/v1/movies-theater', tags=['movies-theater'])
app.include_router(inTheaters, prefix='/api/v1/in-theater', tags=['in-theater'])
