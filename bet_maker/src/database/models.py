import uuid

from sqlalchemy import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()


class BetModel(Base):
    __tablename__ = 'bets'

    uid: Mapped[uuid.UUID] = mapped_column(type_=UUID, primary_key=True, nullable=False)
    event_id: Mapped[str]
    amount: Mapped[float]
    status: Mapped[int]
