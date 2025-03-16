from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class SignupResponse(BaseModel):
    message: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class N(BaseModel):
    message: str
