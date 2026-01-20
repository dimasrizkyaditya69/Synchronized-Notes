from services.supabase_client import supabase


def create_page(workspace_id, title, content="", due_date=None):
    data = {
        "workspace_id": workspace_id,
        "title": title,
        "content": content,
        "due_date": due_date
    }
    return supabase.table("pages").insert(data).execute()

def get_pages(workspace_id):
    return supabase.table("pages").select("*").eq("workspace_id", workspace_id).execute()

def update_page(page_id, **kwargs):
    return supabase.table("pages").update(kwargs).eq("id", page_id).execute()

def delete_page(page_id):
    return supabase.table("pages").delete().eq("id", page_id).execute()

def get_page_by_id(page_id):
    res = supabase.table("pages").select("*").eq("id", page_id).single().execute()
    return res.data

def update_page(page_id, **fields):
    return supabase.table("pages").update(fields).eq("id", page_id).execute()

def delete_page(page_id):
    return supabase.table("pages").delete().eq("id", page_id).execute()
