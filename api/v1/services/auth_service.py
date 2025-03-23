from fastapi import HTTPException
from gotrue.types import User
from supabase import Client

from api.exceptions import (
    EmailNotConfirmedException,
    InvalidCredentialsException,
    NewPasswordsDoNotMatchException,
    OldPasswordIncorrectException,
    PasswordRequirementsException,
    UserAlreadyExistsException,
)
from api.v1.schemas import auth as auth_schemas


def signup_with_email_password(
    supabase_client: Client, user_create: auth_schemas.UserCreate
) -> auth_schemas.SignupResponse:
    """
    Signs up a user with email and password using Supabase Auth.
    """
    try:
        response = supabase_client.auth.sign_up(
            {"email": user_create.email, "password": user_create.password}
        )

        if response.user:
            if not response.user.user_metadata:
                raise UserAlreadyExistsException()

            return auth_schemas.SignupResponse(
                message="Signup successful"
            )

        else:
            raise Exception("Signup failed, no user returned")
    except UserAlreadyExistsException:
        raise UserAlreadyExistsException()
    except Exception as e:
        if "Password should contain at least one character" in str(e):
            raise PasswordRequirementsException()
        raise HTTPException(status_code=500, detail=str(e))


def login_with_email_password(
    supabase_client: Client, email: str, password: str
) -> auth_schemas.LoginResponse:
    """
    Logs in a user with email and password using Supabase Auth.
    """
    try:
        response = supabase_client.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
        if response.session:
            return auth_schemas.LoginResponse(
                access_token=response.session.access_token,
                refresh_token=response.session.refresh_token,
            )
        else:
            raise InvalidCredentialsException()
    except Exception as e:
        # if str(e) == "Email not confirmed":
        #     raise EmailNotConfirmedException()
        raise InvalidCredentialsException()


def refresh_token(
    supabase_client: Client, refresh_token: str
) -> auth_schemas.LoginResponse:
    """
    Logs in a user with email and password using Supabase Auth.
    """
    try:
        response = supabase_client.auth.refresh_session(refresh_token)
        if response.session:
            return auth_schemas.LoginResponse(
                access_token=response.session.access_token,
                refresh_token=response.session.refresh_token,
            )
        else:
            raise InvalidCredentialsException()
    except Exception as e:
        raise InvalidCredentialsException()


def logout(supabase_client: Client, jwt_token: str) -> None:
    """
    Logs out a user using Supabase Auth.
    """
    try:
        supabase_client.auth.admin.sign_out(jwt_token)
    except Exception as e:
        raise e


def change_password(
    supabase_client: Client,
    user: User,
    old_password: str,
    new_password: str,
    confirm_password: str,
) -> None:
    """
    Changes the password of a user using Supabase Auth.
    """
    # Verify old password
    try:
        login_with_email_password(supabase_client, user.email or "", old_password)
    except InvalidCredentialsException:
        raise OldPasswordIncorrectException()

    # Check if new passwords match
    if new_password != confirm_password:
        raise NewPasswordsDoNotMatchException()

    try:
        supabase_client.auth.update_user({"password": new_password})

    except OldPasswordIncorrectException:
        raise OldPasswordIncorrectException()
    except NewPasswordsDoNotMatchException:
        raise NewPasswordsDoNotMatchException()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def forgot_password(supabase_client: Client, email: str) -> None:
    """
    Sends a password reset email to the user.
    """
    try:
        supabase_client.auth.reset_password_for_email(email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
