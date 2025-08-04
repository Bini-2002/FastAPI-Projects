from fastapi import APIRouter , Depends , HTTPException
from typing import Annotated
from httpx import get
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Todos, Users
from fastapi import HTTPException , status , Path
from pydantic import BaseModel, Field
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
  prefix="/user",
  tags=["user"],
)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db_dependancy = Annotated[Session, Depends(get_db)]
user_dependancy = Annotated[dict , Depends(get_current_user)]

class UserVerification(BaseModel):
   password: str = Field(min_length=6)
   new_password: str = Field(min_length=6)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependancy, db: db_dependancy):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(user: user_dependancy, db: db_dependancy, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    db_user = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail='Invalid password')
    db_user.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(db_user)  # Add the updated user to the session
    db.commit()
   