import json
import os
import shutil
import tempfile
from datetime import datetime
from uuid import uuid4

from fastapi import HTTPException
from pytz import timezone
from supabase import Client

from api.v1.schemas.analyze import AnalyzeResponse
from api.v1.services.gemini_service import analyze_image
from utils.image_utils import isImage


async def process_food_analysis(
    file, description, current_user, supabase_client: Client
) -> AnalyzeResponse:
    """Handles image processing, analysis, and database storage."""

    imageType = isImage(file)
    if not imageType:
        raise HTTPException(
            status_code=400,
            detail="Invalid image file. Please upload a valid image (JPG, PNG).",
        )

    try:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".jpg" if imageType == "image/jpeg" else ".png"
        ) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name

        if not os.path.exists(temp_file_path):
            raise HTTPException(status_code=500, detail="Error saving the image.")

        response_json: str = analyze_image(temp_file_path, imageType, description)
        response_dict: dict = json.loads(response_json)

        bucket_name = "user-images"
        unique_filename = f"{current_user.id}_{uuid4()}.{'jpg' if imageType == 'image/jpeg' else 'png'}"

        with open(temp_file_path, "rb") as image_file:
            supabase_client.storage.from_(bucket_name).upload(
                unique_filename, image_file, {"content-type": imageType}
            )

        public_url = supabase_client.storage.from_(bucket_name).get_public_url(
            unique_filename
        )

        utc_tz = timezone("UTC")
        current_time_utc = datetime.now(utc_tz).isoformat()

        data = {
            "user_id": current_user.id,
            "image_url": public_url,
            "food_name": response_dict.get("food_name"),
            "calories": response_dict.get("calories"),
            "protein": response_dict.get("protein"),
            "carbohydrates": response_dict.get("carbohydrates"),
            "fat": response_dict.get("fat"),
            "fiber": response_dict.get("fiber"),
            "sugar": response_dict.get("sugar"),
            "created_at": current_time_utc,
        }

        response = supabase_client.table("food_analysis_results").insert(data).execute()

        # if response.get("status_code") not in [200, 201]:  # type: ignore
        #     raise HTTPException(
        #         status_code=500, detail="Failed to save image metadata."
        #     )

        os.remove(temp_file_path)

        return AnalyzeResponse(**response_dict)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
