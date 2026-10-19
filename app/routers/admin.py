from fastapi import APIRouter, Depends

from app.core.permissions import require_roles
from app.models.users import User

router = APIRouter(
    prefix="/api/admin",
    tags=["Admin"],
)


@router.get("/dashboard")
def admin_dashboard(
    current_user: User = Depends(require_roles("Admin")),
):
    return {
        "message": "Welcome to the admin dashboard",
        "username": current_user.username,
        "role": current_user.role.name,
    }
