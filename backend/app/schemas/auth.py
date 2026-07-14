from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.enums import RolUtilizator


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    rol: RolUtilizator = RolUtilizator.proiectant


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    rol: RolUtilizator


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
