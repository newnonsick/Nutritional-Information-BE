from typing import Optional

from pydantic import BaseModel


class AnalyzeResponse(BaseModel):
    is_food: bool
    food_name: Optional[str] = None
    calories: Optional[int] = None
    protein: Optional[int] = None
    carbohydrates: Optional[int] = None
    fat: Optional[int] = None
    fiber: Optional[int] = None
    sugar: Optional[int] = None
    message: Optional[str] = None
