from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from server.class_market import Market
from server.schemas.schemas_market import SchemaMarketPut

router = APIRouter(tags=["Market"])
market = Market()


@router.get("/")
async def router_market():
    return {"market": market.get_stock()}


@router.post("/sell")
async def router_market(element: SchemaMarketPut, response: Response):
    market.add_to_stock(
        element=element.element,
        cost=element.cost,
        count=element.count,
    )
    response.status_code = status.HTTP_201_CREATED


@router.post("/buy")
async def router_market(element: SchemaMarketPut, response: Response):
    success = market.buy_from_stock(
        element=element.element,
        cost=element.cost,
        count=element.count,
    )
    if success:
        response.status_code = status.HTTP_201_CREATED
    else:
        response.status_code = status.HTTP_403_FORBIDDEN
