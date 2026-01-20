from services.supabase_client import supabase


def get_workspaces(user_id):
    return (
        supabase
        .table("workspaces")
        .select("*")
        .eq("owner", user_id)
        .execute()
    )


def create_workspace(name, user_id):
    return (
        supabase
        .table("workspaces")
        .insert({
            "name": name,
            "owner": user_id
        })
        .execute()
    )


def delete_workspace(workspace_id, user_id):
    return (
        supabase
        .table("workspaces")
        .delete()
        .eq("id", workspace_id)
        .eq("owner", user_id)
        .execute()
    )
