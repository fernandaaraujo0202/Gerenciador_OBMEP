from supabase import create_client

SUPABASE_URL = "https://xyz.supabase.co"  # cole aqui seu Project URL
SUPABASE_KEY = "YOUR_SUPABASE_ANON_KEY"   # cole aqui sua anon/public key

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
