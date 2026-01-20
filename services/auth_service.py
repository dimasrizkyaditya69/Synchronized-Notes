from services.supabase_client import supabase


def register(email, password):
    try:
        res = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        return res
    except Exception as e:
        return {"error": str(e)}

def login(email, password):
    res = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

    # inject token biar RLS jalan
    if res.session:
        supabase.postgrest.auth(res.session.access_token)

    return res.session, res.user

def get_current_user():
    try:
        session = supabase.auth.get_session()
        if session and session.user:
            return session.user
        return None
    except Exception as e:
        return {"error": str(e)}
