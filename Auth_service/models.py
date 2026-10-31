from pydantic import BaseModel, EmailStr, ConfigDict, Field

class RegisterUser(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class LoginUser(BaseModel):
    email: EmailStr

    password: str

# API response
class UserResponse(BaseModel):

    id: int

    name: str

    email: EmailStr

    role: str

    is_active: bool

    model_config = ConfigDict(from_attributes=True)   #This tells Pydantic that it can read values directly from an object's attributes.


# JWT response
class TokenResponse(BaseModel):

    access_token: str

    token_type: str = "bearer"


