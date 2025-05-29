from datetime import datetime, timedelta

import pytz
from fastapi import HTTPException
from gotrue.types import User
from supabase import Client

from api.exceptions import InvalidCredentialsException
from api.v1.schemas.meals import ListMealResponse, MealResponse


def is_meal_owner(meal: dict, user: User) -> bool:
    return meal["user_id"] == user.id


def get_meal_by_id(
    id: str,
    user: User,
    supabase_client: Client,
) -> MealResponse:
    try:
        response = supabase_client.rpc(
            "get_food_analysis_result", {"p_id": id}
        ).execute()

        response_data = response.data

        return MealResponse(
            id=response_data.get("id"),
            image_url=response_data.get("image_url"),
            food_name_en=response_data.get("food_name_en"),
            food_name_th=response_data.get("food_name_th"),
            food_components=response_data.get("food_components", []),
            total_calories=response_data.get("total_calories"),
            total_protein=response_data.get("total_protein"),
            total_carbohydrates=response_data.get("total_carbohydrates"),
            total_fat=response_data.get("total_fat"),
            total_fiber=response_data.get("total_fiber"),
            total_sugar=response_data.get("total_sugar"),
            created_at=response_data.get("created_at"),
        )

    except InvalidCredentialsException:
        raise
    except Exception as e:
        print(f"Error retrieving meal by ID: {e}")
        raise HTTPException(status_code=404, detail="Meal not found")


def get_meals_by_date(
    date: str,
    timezone: str,
    user,
    supabase_client: Client,
) -> ListMealResponse:
    try:
        local_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid date format. Use YYYY-MM-DD."
        )

    try:
        tz = pytz.timezone(timezone)
        start_of_day = tz.localize(
            local_date.replace(hour=0, minute=0, second=0, microsecond=0)
        )
        end_of_day = start_of_day + timedelta(days=1)

        start_of_day_utc = start_of_day.astimezone(pytz.UTC).isoformat()
        end_of_day_utc = end_of_day.astimezone(pytz.UTC).isoformat()
    except Exception:
        raise HTTPException(
            status_code=400, detail="Invalid timezone. Use a valid timezone string."
        )

    try:
        response = supabase_client.rpc(
            "get_food_analysis_results_by_user_and_date",
            {
                "p_user_id": user.id,
                "p_start_date": start_of_day_utc,
                "p_end_date": end_of_day_utc,
            },
        ).execute()

        response_data = response.data

        return ListMealResponse(
            meals=(
                [
                    MealResponse(
                        id=meal.get("id"),
                        image_url=meal.get("image_url"),
                        food_name_en=meal.get("food_name_en"),
                        food_name_th=meal.get("food_name_th"),
                        food_components=meal.get("food_components", []),
                        total_calories=meal.get("total_calories"),
                        total_protein=meal.get("total_protein"),
                        total_carbohydrates=meal.get("total_carbohydrates"),
                        total_fat=meal.get("total_fat"),
                        total_fiber=meal.get("total_fiber"),
                        total_sugar=meal.get("total_sugar"),
                        created_at=meal.get("created_at"),
                    )
                    for meal in response_data
                ]
                if response_data
                else []
            )
        )

    except Exception as e:
        print(f"Error retrieving meals: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving meals.")


def get_all_meals(
    user: User,
    supabase_client: Client,
) -> ListMealResponse:
    try:
        response = supabase_client.rpc(
            "get_food_analysis_results_by_user", {"p_user_id": user.id}
        ).execute()
        response_data = response.data

        return ListMealResponse(
            meals=(
                [
                    MealResponse(
                        id=meal.get("id"),
                        image_url=meal.get("image_url"),
                        food_name_en=meal.get("food_name_en"),
                        food_name_th=meal.get("food_name_th"),
                        food_components=meal.get("food_components", []),
                        total_calories=meal.get("total_calories"),
                        total_protein=meal.get("total_protein"),
                        total_carbohydrates=meal.get("total_carbohydrates"),
                        total_fat=meal.get("total_fat"),
                        total_fiber=meal.get("total_fiber"),
                        total_sugar=meal.get("total_sugar"),
                        created_at=meal.get("created_at"),
                    )
                    for meal in response_data
                ]
                if response_data
                else []
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving meals.")
