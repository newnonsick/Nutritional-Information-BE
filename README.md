# Food Nutritional Information API

This project provides an API to analyze food images and return nutritional information. It uses FastAPI for the web framework and integrates with the Gemini API for image analysis.

## Project Structure

```
.
├── .env
├── .gitignore
├── main.py
├── requirements.txt
├── api/
│   ├── __init__.py
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   └── analyze.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── analyze.py
│   │   └── services/
│   │       ├── __init__.py
│   │       └── gemini.py
├── core/
│   ├── __init__.py
│   ├── config.py
│   ├── logging.py
│   ├── middleware.py
├── utils/
│   ├── __init__.py
│   └── image_utils.py
```

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/newnonsick/Nutritional-Information.git
    cd nutritional-information
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your Gemini API key:
    ```env
    GEMINI_API_KEY=your_gemini_api_key
    ```

## Running the Application

To run the FastAPI application, use the following command:
```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API documentation will be available at `http://127.0.0.1:8000/documentation`.

## API Endpoints

### Analyze Food Image

- **URL:** `/api/v1/analyze`
- **Method:** `POST`
- **Request:**
    - `file`: Upload an image file (JPG, PNG).
    - `description`: (Optional) A brief description of the image or any additional information you want to provide.
- **Response:**
    - `is_food`: Boolean indicating if the image contains food.
    - `food_name`: Name of the food in Thai (if food is detected).
    - `calories`, `protein`, `carbohydrates`, `fat`, `fiber`, `sugar`: Nutritional information (if food is detected).
    - `message`: Description if the image does not contain food.

Example request using `curl`:
```sh
curl -X POST "http://127.0.0.1:8000/api/v1/analyze" -F "file=@path_to_your_image.jpg"
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.