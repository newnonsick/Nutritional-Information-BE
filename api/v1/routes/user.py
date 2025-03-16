from fastapi import APIRouter, Depends
from gotrue.types import User

from api.dependencies import get_current_user

router = APIRouter()


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
