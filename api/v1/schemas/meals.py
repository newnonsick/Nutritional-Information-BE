from pydantic import BaseModel

class FoodComponent(BaseModel):
    id: str
    name_en: str
    name_th: str
    calories: int
    protein: int
    carbohydrates: int
    fat: int
    fiber: int
    sugar: int

class MealResponse(BaseModel):
    id: str
    image_url: str
    food_name_en: str
    food_name_th: str
    food_components: list[FoodComponent]
    total_calories: int
    total_protein: int
    total_carbohydrates: int
    total_fat: int
    total_fiber: int
    total_sugar: int
    created_at: str


class ListMealResponse(BaseModel):
    meals: list[MealResponse]
