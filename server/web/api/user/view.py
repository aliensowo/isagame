from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from server.class_user import User

router = APIRouter(tags=["User"])


@router.get("/")
async def router_market():
    return {"user": None}
