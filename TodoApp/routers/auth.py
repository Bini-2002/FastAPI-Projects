from venv import create
from fastapi import APIRouter, Depends , status
from pydantic import BaseModel
from app.models import Users
from passlib.context import CryptContext
from app.database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session


router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


db_dependancy = Annotated[Session, Depends(get_db)]


@router.post("/auth/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependancy, 
                      create_user_request: CreateUserRequest):
    create_user_model = Users(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password),  # In a real app, hash the password
        role=create_user_request.role,
        is_active=True
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)  # Refresh the instance to get the updated state from the database


