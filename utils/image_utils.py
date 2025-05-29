from io import BytesIO
import os
import shutil
import tempfile

from fastapi import HTTPException, UploadFile
from PIL import Image


def isImage(file: UploadFile) -> str | None:
    """Check if the uploaded file is a valid image."""
    if file.content_type is None or file.content_type not in [
        "image/jpeg",
        "image/png",
    ]:
        return None
    try:
        file.file.seek(0)
        image = Image.open(BytesIO(file.file.read()))
        image.verify()
        file.file.seek(0)
        return file.content_type
    except Exception:
        return None


def save_temp_file(file: UploadFile, image_type: str) -> str:
    """Saves the uploaded file to a temporary location."""
    try:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".jpg" if image_type == "image/jpeg" else ".png"
        ) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            return temp_file.name
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving the image: {str(e)}")


def cleanup_temp_file(temp_file_path: str):
    """Removes the temporary file."""
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)

def reduce_image_size(image_path: str, max_size: tuple[int, int] = (256, 256)):
    """Reduces the image size to the specified dimensions."""
    try:
        with Image.open(image_path) as img:
            img.thumbnail(max_size)
            img.save(image_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reducing image size: {str(e)}")
