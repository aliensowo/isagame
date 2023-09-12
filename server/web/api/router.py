from fastapi.routing import APIRouter
from server.web.api.market import router as market_router
from server.web.api.user import router as user_router

api_router = APIRouter()
api_router.include_router(market_router, prefix="/market")
api_router.include_router(user_router, prefix="/user")
