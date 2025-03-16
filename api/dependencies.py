from fastapi import Depends, Header, HTTPException, status
from supabase import Client

from core.supabase import get_supabase_client


async def get_current_user(
    supabase_client: Client = Depends(get_supabase_client),
    authorization: str = Header(alias="Authorization"),
):
    """
    Dependency to get the current user from a JWT token.
    This verifies the JWT provided in the Authorization header against Supabase.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise credentials_exception

        user = supabase_client.auth.get_user(token)

        if not user or not user.user:
            raise credentials_exception
        return user.user

    except Exception as e:
        raise credentials_exception
