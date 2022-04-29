from fastapi import FastAPI
from app.api.casts import casts
from app.api.database import engine
from app.api import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_url="/api/v1/casts/openapi.json", docs_url="/api/v1/casts/docs")

app.include_router(casts, prefix='/api/v1/casts', tags=['casts'])
