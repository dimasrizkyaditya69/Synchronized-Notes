from services.supabase_client import supabase

resp = supabase.auth.admin.list_users()
print(resp)
