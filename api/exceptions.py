from fastapi import HTTPException, status


class CustomAPIException(HTTPException):
    """Base class for custom API exceptions."""

    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class InvalidCredentialsException(CustomAPIException):
    def __init__(self, detail="Invalid credentials"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class UserAlreadyExistsException(CustomAPIException):
    def __init__(self, detail="User with this email already exists"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class EmailNotConfirmedException(CustomAPIException):
    def __init__(self, detail="Please confirm your email"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class NewPasswordsDoNotMatchException(CustomAPIException):
    def __init__(self, detail="New password and confirm password do not match"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class OldPasswordIncorrectException(CustomAPIException):
    def __init__(self, detail="Old password is incorrect"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
