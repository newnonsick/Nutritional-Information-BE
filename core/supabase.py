from supabase import create_client, Client
from core.config import settings


def get_supabase_client() -> Client:
    """
    Creates and returns a Supabase client instance.
    """
    supabase_url = settings.SUPABASE_URL
    supabase_anon_key = settings.SUPABASE_ANON_KEY
    if not supabase_url or not supabase_anon_key:
        raise ValueError(
            "Supabase URL and Anon Key must be set in environment variables."
        )
    return create_client(supabase_url, supabase_anon_key)
