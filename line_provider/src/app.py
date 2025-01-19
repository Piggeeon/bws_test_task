import aiohttp
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from src.config import BET_MAKER_CHANGE_STATE_URL
from src.schemas import EventSchema, EventState
from src.services.events_service import EventsService

LOGGER = logging.getLogger(__name__)

app = FastAPI()
events_service = EventsService()


@app.put('/event')
async def create_event(event: EventSchema):
    await events_service.add_event(event=event)
    LOGGER.info(f"Event created: {event}")

    return JSONResponse(content={"message": "Event created successfully", "event_id": event.id}, status_code=201)


@app.patch('/event/{event_id}')
async def change_event_state(event_id: str, new_state: EventState):
    LOGGER.info(f"Changing state of event {event_id} to {new_state}.")
    await events_service.change_event_state(event_id=event_id, new_state=new_state)

    async with aiohttp.ClientSession() as new_session:
        async with new_session.patch(url=BET_MAKER_CHANGE_STATE_URL,
                                     params={"event_id": event_id, "new_state": new_state}) as response:
            if response.status == 200:
                LOGGER.info(f"Successfully changed state for event {event_id} in bet_maker service.")
                return JSONResponse(content={"message": "Event state changed successfully"}, status_code=200)
            else:
                LOGGER.error(f"Error from bet_maker service: {response.status}")
                raise HTTPException(status_code=response.status, detail="Error with bet_maker service")


@app.get('/event/{event_id}')
async def get_event(event_id: str) -> EventSchema:
    LOGGER.info(f"Fetching event with ID: {event_id}.")

    event = await events_service.get_event(event_id=event_id)
    if event:
        LOGGER.info(f"Event found: {event}")
        return event

    LOGGER.info(f"Event not found: {event_id}.")
    raise HTTPException(status_code=404, detail="Event not found")


@app.get('/events')
async def get_events() -> list[EventSchema]:
    LOGGER.info("Fetching all actual events.")

    events = await events_service.get_events()

    LOGGER.info(f"Total events retrieved: {len(events)}.")

    return events
