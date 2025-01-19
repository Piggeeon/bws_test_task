import uuid

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from src.database.db_core import DatabaseCore
from src.config import DATABASE_URL
from src.schemas import BetSchema, EventState, EventSchema
from src.services.bets_service import BetsService
from src.database.repositories.bets_repository import BetsRepository
from src.config import LINE_PROVIDER_GET_EVENTS_URL
import logging
import aiohttp


LOGGER = logging.getLogger(__name__)


app = FastAPI()
db_core = DatabaseCore(url=DATABASE_URL)


@app.on_event("startup")
async def on_startup():
    await db_core.create_tables()
    LOGGER.info("Database tables created on startup.")


@app.post("/bet")
async def place_bet(event_id: str, amount: float, session=Depends(db_core.get_session)):
    async with aiohttp.ClientSession() as new_session:
        LOGGER.info(f"Fetching events from {LINE_PROVIDER_GET_EVENTS_URL}.")

        async with new_session.get(url=LINE_PROVIDER_GET_EVENTS_URL) as response:
            events = await response.json()

    if response.status != 200:
        LOGGER.error("Failed to fetch events")
        raise HTTPException(status_code=500, detail="Cant get events from line_provider")

    if not any(event['id'] == event_id for event in events):
        LOGGER.info(f"Event ID {event_id} not found in fetched events.")
        raise HTTPException(status_code=404, detail="Event not found in fetched events")

    bets_repository = BetsRepository(session=session)
    bets_service = BetsService(bets_repository=bets_repository)
    bet = BetSchema(uid=uuid.uuid4(), event_id=event_id, amount=amount, status=EventState.NEW)
    await bets_service.place_bet(bet=bet)
    await session.commit()

    return JSONResponse(content={"message": "Bet placed", "bet_uid": str(bet.uid)}, status_code=201)


@app.patch("/bet")
async def on_change_event_status(event_id: str, new_state: EventState, session=Depends(db_core.get_session)):
    bets_repository = BetsRepository(session=session)
    bets_service = BetsService(bets_repository=bets_repository)
    await bets_service.change_bets_statuses(event_id=event_id, new_status=new_state)
    await session.commit()

    LOGGER.info(f"Bets status changed for event ID {event_id} to {new_state}.")

    return JSONResponse(content={"message": "Bets status updated"}, status_code=200)


@app.get("/bets")
async def get_bets(session=Depends(db_core.get_session)):
    bets_repository = BetsRepository(session=session)
    bets_service = BetsService(bets_repository=bets_repository)
    bets = await bets_service.get_bets()

    LOGGER.info(f"Fetched {len(bets)} bets.")

    return bets


@app.get("/events")
async def get_events() -> list[EventSchema]:
    async with aiohttp.ClientSession() as new_session:
        LOGGER.info(f"Fetching events from {LINE_PROVIDER_GET_EVENTS_URL}.")

        async with new_session.get(url=LINE_PROVIDER_GET_EVENTS_URL) as response:
            events = await response.json()

            if response.status != 200:
                LOGGER.error(f"Failed to fetch events with status: {response.status}")
                raise HTTPException(status_code=response.status, detail="Cant get events from line_provider")

    LOGGER.info(f"Fetched {len(events)} events.")

    return events
