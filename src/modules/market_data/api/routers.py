from fastapi import APIRouter, FastAPI, Depends
from shared.dispatching.abstractions import Dispatcher
from market_data.application.commands import CreateUserCommand
from market_data.application.queries import HelloQuery
from shared.di.fastapi import inject

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
    symbol: str,
    quantity: int,
    dispatcher: Dispatcher = Depends(inject(Dispatcher))
):
    command = CreateUserCommand("aaa")  # à remplacer par un vrai DTO
    await dispatcher.send_async(command)
    return {"status": "ok"}


def get_router() -> APIRouter:
    return router


def initialize(app: FastAPI) -> None:
    print("Market Data module initialized")
