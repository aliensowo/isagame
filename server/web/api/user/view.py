from fastapi import APIRouter

router = APIRouter(tags=["User"])


@router.get("/")
async def router_market():
    return {"user": None}
