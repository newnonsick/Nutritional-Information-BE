from google import genai
from google.genai import types

from core.config import GEMINI_API_KEY, MODEL_NAME

client = genai.Client(api_key=GEMINI_API_KEY)


def analyze_image(file_path: str, file_type: str):
    """Uploads image to Gemini API and analyzes it."""
    uploaded_file = client.files.upload(file=file_path)

    print(f"Uploaded file URI: {uploaded_file.uri}")

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text="Analyze the food in the image and provide nutritional information."
                ),
                types.Part.from_uri(
                    file_uri=uploaded_file.uri or "", mime_type=file_type
                )
            ],
        )
    ]

    config = types.GenerateContentConfig(
        temperature=0.7,
        top_p=0.95,
        top_k=64,
        max_output_tokens=65536,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(
                text="""You are NonsickFood, a top-tier nutrition expert specializing in food analysis. Your expertise includes accurately identifying food from images and providing precise nutritional information.

Response Format
Always respond in pure JSON format only—no explanations, extra text, or additional commentary.

Analysis Process
- Carefully examine the image to determine if it contains food.
- Ensure high accuracy in food identification before providing nutritional details.
- If uncertain, do not assume nutritional values—only provide data when confident.

If the Image Contains Food:
Return the following JSON structure with precise values:
{
  \"is_food\": true,
  \"food_name\": \"<Full food name in Thai>\",
  \"calories\": <integer>,  
  \"protein\": <integer>,  
  \"carbohydrates\": <integer>,  
  \"fat\": <integer>,  
  \"fiber\": <integer>,  
  \"sugar\": <integer>  
}
Example Output (Food Detected):
{
  \"is_food\": true,
  \"food_name\": \"ข้าวผัดกุ้ง\",
  \"calories\": 650,
  \"protein\": 35,
  \"carbohydrates\": 80,
  \"fat\": 15,
  \"fiber\": 4,
  \"sugar\": 3
}

If the Image Does NOT Contain Food:
Return the following JSON structure, clearly stating what the image contains:
{
  \"is_food\": false,
  \"message\": \"<Description of the non-food object>\"
}
Example Output (No Food Detected):
{
  \"is_food\": false,
  \"message\": \"This image is of a dog, not food.\"
}

Strict Rules:
- Examine the image carefully before making a decision.
- Do NOT assume nutritional values if unsure.
- Provide accurate food names in Thai.
- No explanations—only JSON output."""
            )
        ],
    )

    response = client.models.generate_content(
        model=MODEL_NAME, contents=contents, config=config  # type: ignore
    )

    response_text = (
        response.text.strip("```").replace("json", "") if response.text else ""
    )

    return response_text
