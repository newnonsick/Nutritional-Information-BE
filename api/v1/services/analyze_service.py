import json
from datetime import datetime
from typing import Optional
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from gotrue.types import User
from pytz import timezone
from supabase import Client

from api.exceptions import NotFoodImageException
from api.v1.schemas.meals import FoodComponent, MealResponse
from api.v1.services.gemini_service import analyze_image
from utils.image_utils import (
    cleanup_temp_file,
    isImage,
    reduce_image_size,
    save_temp_file,
)


def process_food_analysis(
    file: UploadFile,
    user: User,
    supabase_client: Client,
    description: Optional[str] = None,
) -> MealResponse:
    """Handles image processing, analysis, and database storage."""

    image_type = isImage(file)
    if not image_type:
        raise HTTPException(
            status_code=400,
            detail="Invalid image file. Please upload a valid image (JPG, PNG).",
        )

    temp_file_path = save_temp_file(file, image_type)

    try:
        response_dict = _analyze_image_and_parse_response(
            temp_file_path, image_type, description
        )

        if response_dict.get("is_food", False):
            for component in response_dict.get("food_components", []):
                uuid4_str = str(uuid4())
                component["id"] = uuid4_str

            public_url, data_id, created_at = _store_image_and_metadata(
                temp_file_path, image_type, user, supabase_client, response_dict
            )

            return _build_analyze_response(
                response_dict, data_id, public_url, created_at
            )
        else:
            raise NotFoodImageException(
                detail=response_dict.get(
                    "message", "Invalid image. Please upload an image of food."
                ),
            )

    except NotFoodImageException as e:
        raise NotFoodImageException(
            detail=e.detail,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cleanup_temp_file(temp_file_path)


def _analyze_image_and_parse_response(
    temp_file_path: str, image_type: str, description: Optional[str]
) -> dict:
    """Analyzes the image and parses the response."""
    response_json = analyze_image(temp_file_path, image_type, description)
    return json.loads(response_json)


def _store_image_and_metadata(
    temp_file_path: str,
    image_type: str,
    user: User,
    supabase_client: Client,
    response_dict: dict,
) -> tuple[str, str, str]:
    """Stores the image in the storage bucket and saves metadata in the database."""
    bucket_name = "user-images"
    unique_filename = (
        f"{user.id}_{uuid4()}.{'jpg' if image_type == 'image/jpeg' else 'png'}"
    )

    reduce_image_size(temp_file_path)

    with open(temp_file_path, "rb") as image_file:
        supabase_client.storage.from_(bucket_name).upload(
            unique_filename, image_file, {"content-type": image_type}
        )

    public_url = supabase_client.storage.from_(bucket_name).get_public_url(
        unique_filename
    )

    data_id = str(uuid4())
    current_time_utc = _save_metadata_to_db(
        user, supabase_client, public_url, response_dict, data_id
    )

    return public_url, data_id, current_time_utc


def _save_metadata_to_db(
    user: User,
    supabase_client: Client,
    public_url: str,
    response_dict: dict,
    data_id: str,
) -> str:
    """Saves the metadata of the analyzed image to the database."""

    current_time_utc = datetime.now(timezone("UTC")).isoformat()

    supabase_client.rpc(
        "insert_food_analysis_with_components",
        {
            "_id": data_id,
            "_user_id": user.id,
            "_food_name_en": response_dict.get("food_name_en"),
            "_food_name_th": response_dict.get("food_name_th"),
            "_image_url": public_url,
            "_created_at": current_time_utc,
            "_food_components": response_dict.get("food_components", []),
        },
    ).execute()

    return current_time_utc


def _build_analyze_response(
    response_dict: dict, data_id: str, image_url: str, created_at: str
) -> MealResponse:
    """Builds the MealResponse object."""
    food_components: list[FoodComponent] = [
        FoodComponent(**component)
        for component in response_dict.get("food_components", [])
    ]

    return MealResponse(
        id=data_id,
        image_url=image_url,
        food_name_en=response_dict.get("food_name_en", ""),
        food_name_th=response_dict.get("food_name_th", ""),
        food_components=food_components,
        total_calories=response_dict.get("total_calories", 0),
        total_protein=response_dict.get("total_protein", 0),
        total_carbohydrates=response_dict.get("total_carbohydrates", 0),
        total_fat=response_dict.get("total_fat", 0),
        total_fiber=response_dict.get("total_fiber", 0),
        total_sugar=response_dict.get("total_sugar", 0),
        created_at=created_at,
    )
