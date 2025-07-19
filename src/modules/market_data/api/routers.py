from fastapi import APIRouter, FastAPI, Depends
from shared.dispatching.abstractions import Dispatcher
from market_data.application.commands import CreateMarketData
from market_data.application.queries import HelloQuery
from shared.di.fastapi import inject
from market_data.application.dto import MarketDataRequestDto


MODULE_CONFIG = {
    "prefix": "/api/market-data",
    "tags": ["Market Data"]
}

router = APIRouter()


@router.get("/ping")
def ping():
    return {"message": "Market Data module is alive"}


@router.get("/hello")
async def say_hello(
    name: str = "World",
    dispatcher: Dispatcher = Depends(inject(Dispatcher))
) -> str:
    query = HelloQuery(name)
    result = await dispatcher.query_async(query)
    return result


@router.post("/create-market-data")
async def create_order(
    dto: MarketDataRequestDto,
    dispatcher: Dispatcher = Depends(inject(Dispatcher))
):
    command = CreateMarketData(dto.symbol, dto.price)
    await dispatcher.send_async(command)
    return {"status": "ok"}


def get_router() -> APIRouter:
    return router


def initialize(app: FastAPI) -> None:
    print("Market Data module initialized")
