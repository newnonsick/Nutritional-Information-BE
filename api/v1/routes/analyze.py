import asyncio
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from gotrue.types import User
from supabase import Client

from api.dependencies import get_current_user
from api.v1.schemas.analyze import AnalyzeResponse
from api.v1.services.analyze_service import process_food_analysis
from core.supabase import get_supabase_client

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_food(
    current_user: User = Depends(get_current_user),
    supabase_client: Client = Depends(get_supabase_client),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
):
    """Endpoint to analyze food image."""
    return await asyncio.to_thread(
        process_food_analysis, file, current_user, supabase_client, description
    )
