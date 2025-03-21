from supabase import Client, create_client

from core.config import settings



def get_supabase_client() -> Client:

    supabase_url: str | None = settings.SUPABASE_URL
    supabase_key: str | None = settings.SUPABASE_KEY

    if not supabase_url:
        raise ValueError("Missing Supabase URL in environment variables.")
    if not supabase_key:
        raise ValueError("Missing Supabase API key in environment variables.")

    supabase_client = create_client(supabase_url, supabase_key)

    return supabase_client
