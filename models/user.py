from enum import Enum
from dataclasses import dataclass
from pydantic import BaseModel, EmailStr

# Enums
class UserRoles(str, Enum):
    USER = "user"
    ADMIN = "admin"

# Data classes
@dataclass
class UserProfile:
    email: int
    type: UserRoles

# Schemas
class LoginData(BaseModel):
    email: EmailStr
    password: str

class RegisterData(BaseModel):
    email: EmailStr
    password: str
    type: UserRoles