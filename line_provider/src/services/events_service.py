import logging
import time

from src.schemas import EventSchema

LOGGER = logging.getLogger(__name__)


class EventsService:
    def __init__(self):
        self.events: dict[str, EventSchema] = {}

    async def add_event(self, event: EventSchema):
        if event.id not in self.events:
            LOGGER.info(f"Got new event: {event}")
            self.events[event.id] = event
        else:
            LOGGER.info(f"Event already exists, new attributes will be set: {event}")
            for p_name, p_value in event.dict(exclude_unset=True).items():
                setattr(self.events[event.id], p_name, p_value)

    async def change_event_state(self, event_id, new_state):
        self.events[event_id].state = new_state

    async def get_events(self):
        return list(e for e in self.events.values() if time.time() < e.deadline)

    async def get_event(self, event_id):
        if event_id in self.events:
            return self.events[event_id]
