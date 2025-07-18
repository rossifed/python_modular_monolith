from fastapi import APIRouter, FastAPI, Depends
from shared.dispatching.abstractions import Dispatcher
from orders.application.commands import CreateOrderCommand
from orders.application.queries import OrderQuery
from shared.di.fastapi import inject

# Configuration optionnelle du module
MODULE_CONFIG = {
    "prefix": "/api/orders",
    "tags": ["Orders"]
}

router = APIRouter()


@router.get("/ping")
def ping():
    return {"message": "Orders module is alive"}


@router.get("/hello")
async def say_hello(
    name: str = "World",
    dispatcher: Dispatcher = Depends(inject(Dispatcher))
) -> str:
    query = OrderQuery(name)
    result = await dispatcher.query_async(query)
    return result


@router.post("/create-order")
async def create_order(
    symbol: str,
    quantity: int,
    dispatcher: Dispatcher = Depends(inject(Dispatcher))
):
    command = CreateOrderCommand("aaa")  # à adapter plus tard avec un vrai DTO
    await dispatcher.send_async(command)
    return {"status": "ok"}


def get_router() -> APIRouter:
    return router


def initialize(app: FastAPI) -> None:
    print("Orders module initialized")
