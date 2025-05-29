# Food Nutritional Information API

This project provides an API to analyze food images and return nutritional information. It uses FastAPI for the web framework and integrates with the Gemini API for image analysis.

## Project Structure

```
.
├── .env
├── .gitignore
├── LICENSE
├── main.py
├── README.md
├── requirements.txt
├── api/
│   ├── __init__.py
│   ├── dependencies.py
│   ├── exceptions.py
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── user_model.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── analyze.py
│   │   │   ├── auth.py
│   │   │   ├── meals.py
│   │   │   └── user.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── analyze.py
│   │   │   ├── auth.py
│   │   │   └── meals.py
│   │   ├── services/
│   │       ├── __init__.py
│   │       ├── analyze_service.py
│   │       ├── auth_service.py
│   │       ├── gemini_service.py
│   │       └── meals_service.py
├── core/
│   ├── __init__.py
│   ├── config.py
│   ├── logging.py
│   ├── middleware.py
│   └── supabase.py
├── utils/
│   ├── __init__.py
│   └── image_utils.py
```

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/newnonsick/Nutritional-Information-BE.git
    cd nutritional-information-be
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
4. **Set up your Supabase database schema:**

    - Open the [Supabase SQL Editor](https://app.supabase.com/project/_/sql) for your project.
    - Copy the contents of [`initial_schema.sql`](initial_schema.sql) and paste them into a new SQL query.
    - Run the query to create the necessary tables, indexes, and functions.

5. Create a `.env` file in the root directory and add your Gemini API key and Supabase credentials:
    ```env
    GEMINI_API_KEY=your_gemini_api_key
    MODEL_NAME=gemini_model_name
    SUPABASE_URL=your_supabase_url
    SUPABASE_KEY=your_supabase_key (service_role)
    ```

## Running the Application

To run the FastAPI application, use the following command:
```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API documentation will be available at `http://localhost:8000/documentation`.

## API Endpoints

For a detailed list of API endpoints and their usage, please refer to the [API Documentation](http://localhost:8000/documentation).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.