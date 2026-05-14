from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.models.user import Role


# ---------------- Create User ----------------
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)


# ---------------- Login ----------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ---------------- Response ----------------
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: Role
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# ---------------- Optional (BEST PRACTICE) ----------------
class UserPublic(BaseModel):
    """
    Safe version for public APIs (no sensitive data).
    """
    id: int
    username: str
    role: Role

    model_config = ConfigDict(from_attributes=True)