import logging

from sqlalchemy import URL

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logging.basicConfig(level=logging.DEBUG, handlers=[stream_handler])

DATABASE_USER = "postgres"
DATABASE_PASSWORD = "pass"
DATABASE_HOST = "postgres-container"
DATABASE_PORT = 5432
DATABASE_NAME = "bet_maker"
DATABASE_DRIVER = "postgresql+asyncpg"

DATABASE_URL = URL.create(
    drivername=DATABASE_DRIVER,
    username=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=DATABASE_PORT,
    database=DATABASE_NAME,
)

LINE_PROVIDER_GET_EVENTS_URL = "http://line_provider:8000/events"
