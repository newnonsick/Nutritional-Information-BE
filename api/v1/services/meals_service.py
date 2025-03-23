from fastapi import HTTPException
from gotrue.types import User
from supabase import Client

from api.exceptions import InvalidCredentialsException
from api.v1.schemas.meals import ListMealResponse, MealResponse
from datetime import datetime, timedelta


def get_meal_by_id(
    id: str,
    user: User,
    supabase_client: Client,
) -> MealResponse:
    try:
        response = (
            supabase_client.from_("food_analysis_results")
            .select("*")
            .eq("id", id)
            .single()
            .execute()
        )
        response_data = response.data

        if not is_meal_owner(response_data, user):
            raise InvalidCredentialsException()

        return MealResponse(
            id=response_data["id"],
            image_url=response_data["image_url"],
            food_name=response_data["food_name"],
            calories=response_data["calories"],
            protein=response_data["protein"],
            carbohydrates=response_data["carbohydrates"],
            fat=response_data["fat"],
            fiber=response_data["fiber"],
            sugar=response_data["sugar"],
            created_at=response_data["created_at"],
        )
    except InvalidCredentialsException:
        raise
    except Exception as e:
        raise HTTPException(status_code=404, detail="Meal not found")


def is_meal_owner(meal: dict, user: User) -> bool:
    return meal["user_id"] == user.id


def get_meals_by_date(
    date: str,
    user,
    supabase_client: Client,
) -> ListMealResponse:
    try:
        formatted_date = datetime.strptime(date, "%Y-%m-%d")

        start_of_day = formatted_date.strftime("%Y-%m-%d 00:00:00")
        end_of_day = (formatted_date + timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")

    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid date format. Use YYYY-MM-DD."
        )

    try:
        response = (
            supabase_client.from_("food_analysis_results")
            .select("*")
            .eq("user_id", user.id)
            .gte("created_at", start_of_day)
            .lt("created_at", end_of_day)
            .order("created_at", desc=True)
            .execute()
        )

        response_data = response.data

        return ListMealResponse(
            meals=[
                MealResponse(
                    id=meal["id"],
                    image_url=meal["image_url"],
                    food_name=meal["food_name"],
                    calories=meal["calories"],
                    protein=meal["protein"],
                    carbohydrates=meal["carbohydrates"],
                    fat=meal["fat"],
                    fiber=meal["fiber"],
                    sugar=meal["sugar"],
                    created_at=meal["created_at"],
                )
                for meal in response_data
            ]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving meals.")


def get_all_meals(
    user: User,
    supabase_client: Client,
) -> ListMealResponse:
    try:
        response = (
            supabase_client.from_("food_analysis_results")
            .select("*")
            .eq("user_id", user.id)
            .order("created_at", desc=True)
            .execute()
        )
        response_data = response.data

        return ListMealResponse(
            meals=[
                MealResponse(
                    id=meal["id"],
                    image_url=meal["image_url"],
                    food_name=meal["food_name"],
                    calories=meal["calories"],
                    protein=meal["protein"],
                    carbohydrates=meal["carbohydrates"],
                    fat=meal["fat"],
                    fiber=meal["fiber"],
                    sugar=meal["sugar"],
                    created_at=meal["created_at"],
                )
                for meal in response_data
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving meals.")
