

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.core.database import get_db
from app.repositories.user_repo import get_user_by_id
from app.models.user import Role, User


# =========================
# 🔹 Bearer Token (Swagger FIX)
# =========================

oauth2_scheme = HTTPBearer(auto_error=True)


# =========================
# 🔹 Get Current User
# =========================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:

    token = credentials.credentials

    # 1. Decode JWT safely
    try:
        payload = decode_access_token(token)

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token validation failed"
        )

    # 2. Extract user id
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    # 3. Validate format
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token user id"
        )

    # 4. Fetch user
    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    # 5. Active check
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    return user


# =========================
# 🔹 Role-Based Access Control
# =========================

def require_role(*roles: Role):
    """
    RBAC dependency:
    Example: require_role(Role.admin)
    """

    def role_checker(user: User = Depends(get_current_user)):

        if user.role.value not in [r.value for r in roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

        return user

    return role_checker