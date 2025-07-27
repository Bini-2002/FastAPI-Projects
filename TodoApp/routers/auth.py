from venv import create
import bcrypt
from fastapi import APIRouter
from pydantic import BaseModel
from app.models import Users
from passlib.context import CryptContext

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

@router.post("/auth/")
async def create_user(create_user_request : CreateUserRequest):
  create_user_model = Users(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password),  # In a real app, hash the password
        role=create_user_request.role,
        is_active=True
    )
    # Here you would typically add the user to the database
    # For example: db.add(create_user_model)
    # db.commit()
  return create_user_model


