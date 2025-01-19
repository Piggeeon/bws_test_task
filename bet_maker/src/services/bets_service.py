from src.schemas import BetSchema, EventState
from src.database.repositories.bets_repository import BetsRepository


class BetsService:
    def __init__(self, bets_repository: BetsRepository):
        self.bets_repository = bets_repository

    async def place_bet(self, bet: BetSchema):
        await self.bets_repository.place_bet(bet=bet)

    async def change_bets_statuses(self, event_id: str, new_status: EventState):
        await self.bets_repository.change_bets_statuses(event_id=event_id, new_status=new_status)

    async def get_bets(self):
        return await self.bets_repository.get_bets()
