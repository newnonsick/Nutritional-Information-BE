from pydantic import BaseModel
from gotrue.types import User

class CurrentUserModel(BaseModel):
    user: User
    jwt_token: str