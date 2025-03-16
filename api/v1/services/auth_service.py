from fastapi import HTTPException
from supabase import Client

from api.exceptions import (
    EmailNotConfirmedException,
    InvalidCredentialsException,
    UserAlreadyExistsException,
)
from api.v1.schemas import auth as auth_schemas


async def signup_with_email_password(
    supabase_client: Client, user_create: auth_schemas.UserCreate
) -> auth_schemas.SignupResponse:
    """
    Signs up a user with email and password using Supabase Auth.
    """
    try:
        response = supabase_client.auth.sign_up(
            {"email": user_create.email, "password": user_create.password}
        )
        # print(response)
        if response.user:
            if not response.user.user_metadata:
                raise UserAlreadyExistsException()

            return auth_schemas.SignupResponse(
                message="Signup successful, please check your email to confirm your account."
            )

        else:
            raise Exception("Signup failed, no user returned")
    except Exception as e:
        if "duplicate key value violates unique constraint" in str(e).lower():
            raise UserAlreadyExistsException()
        else:
            raise


async def login_with_email_password(
    supabase_client: Client, email: str, password: str
) -> auth_schemas.Token:
    """
    Logs in a user with email and password using Supabase Auth.
    """
    try:
        response = supabase_client.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
        if response.session:
            return auth_schemas.Token(access_token=response.session.access_token)
        else:
            print(1)
            raise InvalidCredentialsException()
    except Exception as e:
        if str(e) == "Email not confirmed":
            raise EmailNotConfirmedException()
        raise InvalidCredentialsException()
