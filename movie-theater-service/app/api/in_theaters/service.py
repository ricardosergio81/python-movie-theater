import os
import httpx
from app.api.movie_theaters import db_manager

MOVIE_SERVICE_HOST_URL = 'http://localhost:8001/api/v1/movies/'
MOVIE_THEATER_SERVICE_HOST_URL = 'http://localhost:8003/api/v1/movies-theater/'

def is_movie_present(movie_id: int):
    url = os.environ.get('MOVIE_SERVICE_HOST_URL') or MOVIE_SERVICE_HOST_URL
    r = httpx.get(f'{url}{movie_id}/')
    return True if r.status_code == 200 else False

def is_movie_theater_present(movie_theater_id: int):
    #url = os.environ.get('MOVIE_THEATER_SERVICE_HOST_URL') or MOVIE_THEATER_SERVICE_HOST_URL
    #r = httpx.get(f'{url}{movie_theater_id}/', timeout=5)
    #return True if r.status_code == 200 else False
    return db_manager.get_movie_theater(movie_theater_id)
