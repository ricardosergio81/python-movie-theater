import os
os.environ["DATABASE_URI"] = "postgresql://movie_db_username:movie_db_password@localhost:5434/movie_db_dev"
os.environ["CAST_SERVICE_HOST_URL"] = 'http://localhost.cast/cast/'
