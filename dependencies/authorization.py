from fastapi import HTTPException, status, Depends
from models.user import UserProfile, UserRoles
from .authentication import get_current_user

class RoleChecker:
    def __init__(self, *allowed_roles: UserRoles):
        self.allowed_roles = allowed_roles

    def __call__(self, user: UserProfile = Depends(get_current_user)):
        if user.type not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have the required permissions"
            )
        return user