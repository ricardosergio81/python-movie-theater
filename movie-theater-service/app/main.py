from fastapi import FastAPI
from app.api.movie_theaters.movies_theaters import moviesTheaters
from app.api.in_theaters.in_theaters import inTheaters
from app.api.db import metadata, engine, database

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/v1/movies-theater/openapi.json", docs_url="/api/v1/movies-theater/docs")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(moviesTheaters, prefix='/api/v1/movies-theater', tags=['movies-theater'])
app.include_router(inTheaters, prefix='/api/v1/in-theater', tags=['in-theater'])