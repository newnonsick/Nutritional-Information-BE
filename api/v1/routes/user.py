from fastapi import APIRouter, Depends
from gotrue.types import User

from api.dependencies import get_current_user
from api.v1.models.user_model import CurrentUserModel

router = APIRouter()


@router.get("/me")
async def read_users_me(current_user: CurrentUserModel = Depends(get_current_user)):
    return current_user.user
