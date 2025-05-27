from pydantic import BaseModel


class MealResponse(BaseModel):
    id: str
    image_url: str
    food_name_en: str
    food_name_th: str
    calories: int
    protein: int
    carbohydrates: int
    fat: int
    fiber: int
    sugar: int
    created_at: str

class ListMealResponse(BaseModel):
    meals: list[MealResponse]