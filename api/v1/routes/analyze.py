import json
import os
import shutil
import tempfile
from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from api.v1.schemas.analyze import AnalyzeResponse
from api.v1.services.gemini import analyze_image
from utils.image_utils import isImage

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_food(
    description: Optional[str] = Form(None), file: UploadFile = File(...)
):
    """Endpoint to analyze food image."""
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

        response_json = analyze_image(temp_file_path, imageType, description)
        response_dict = json.loads(response_json)

        os.remove(temp_file_path)

        return response_dict

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
