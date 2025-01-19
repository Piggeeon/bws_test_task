import decimal
from typing import Optional
from uuid import UUID
import enum
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class EventState(enum.IntEnum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


class EventSchema(BaseModel):
    id: str
    coefficient: Optional[decimal.Decimal] = None
    deadline: Optional[int] = None
    state: Optional[EventState] = None


class BetSchema(BaseSchema):
    uid: UUID
    event_id: str
    amount: float
    status: EventState
