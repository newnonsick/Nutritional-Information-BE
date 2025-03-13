from fastapi import UploadFile
from PIL import Image
from io import BytesIO


@staticmethod
def isImage(file: UploadFile) -> str | None:
    """Check if the uploaded file is a valid image."""
    if file.content_type is None or file.content_type not in ["image/jpeg", "image/png"]:
        return None
    try:
        file.file.seek(0)
        image = Image.open(BytesIO(file.file.read()))
        image.verify()
        file.file.seek(0)
        return file.content_type
    except Exception:
        return None
