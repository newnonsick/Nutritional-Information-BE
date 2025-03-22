from google import genai
from google.genai import types

from core.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def analyze_image(
    file_path: str, file_type: str, description: str | None = None
) -> str:
    """Uploads image to Gemini API and analyzes it."""
    uploaded_file: types.File = client.files.upload(file=file_path)

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=f"Look at the image provided very carefully and carefully analyze the food in the image and tell the nutritional information. {"From here on out, there will be more explanatory material to help you think and make better decisions: " + description if description else ''}"
                ),
                types.Part.from_uri(
                    file_uri=uploaded_file.uri or "", mime_type=file_type
                ),
            ],
        )
    ]

    config = types.GenerateContentConfig(
        temperature=0.7,
        top_p=0.95,
        top_k=64,
        max_output_tokens=65536,
        response_mime_type="text/plain",
        system_instruction=[types.Part.from_text(text=settings.SYSTEM_INSTRUCTION)],
    )

    response = client.models.generate_content(
        model=settings.MODEL_NAME, contents=contents, config=config  # type: ignore
    )

    if uploaded_file.name:
        client.files.delete(name=uploaded_file.name)

    response_text = (
        response.text.strip("```").replace("json", "") if response.text else ""
    )

    return response_text
