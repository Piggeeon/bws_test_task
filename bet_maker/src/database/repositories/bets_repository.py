from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from src.schemas import BetSchema, EventState
from src.database.models import BetModel


class BetsRepository:
    def __init__(self, session):
        self.session: AsyncSession = session

    async def place_bet(self, bet: BetSchema):
        bet = BetModel(**bet.model_dump())
        self.session.add(bet)

    async def change_bets_statuses(self, event_id: str, new_status: EventState):
        await self.session.execute(update(BetModel).where(BetModel.event_id == event_id).values(status=new_status))

    async def get_bets(self) -> list[BetSchema]:
        bets = (await self.session.execute(select(BetModel))).scalars().all()

        return [BetSchema.model_validate(bet) for bet in bets]
