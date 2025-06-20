import asyncio
from typing import Optional

from fastapi import APIRouter, Depends
from supabase import Client

from api.dependencies import get_current_user
from api.v1.models.user_model import CurrentUserModel
from api.v1.schemas.meals import ListMealResponse, MealResponse
from api.v1.services import meals_service
from core.supabase import get_supabase_client

router = APIRouter()


@router.get("/meals/:id", response_model=MealResponse)
async def get_meal_by_id(
    id: str,
    current_user: CurrentUserModel = Depends(get_current_user),
    supabase_client: Client = Depends(get_supabase_client),
):
    return await asyncio.to_thread(
        meals_service.get_meal_by_id, id, current_user.user, supabase_client
    )


@router.get("/meals", response_model=ListMealResponse)
async def get_meals_by_date(
    date: Optional[str] = None,
    timezone: Optional[str] = None,
    current_user: CurrentUserModel = Depends(get_current_user),
    supabase_client: Client = Depends(get_supabase_client),
):

    if date and timezone:
        return await asyncio.to_thread(
            meals_service.get_meals_by_date, date, timezone, current_user.user, supabase_client
        )

    return await asyncio.to_thread(
        meals_service.get_all_meals, current_user.user, supabase_client
    )
