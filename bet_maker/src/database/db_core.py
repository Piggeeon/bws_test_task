from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from src.database.models import Base


class DatabaseCore:
    def __init__(self, url: URL):
        self.url = url
        self.engine = create_async_engine(url, echo=True)
        self.session_factory = async_sessionmaker(bind=self.engine)

    async def get_session(self):
        async with self.session_factory() as session:
            yield session

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
