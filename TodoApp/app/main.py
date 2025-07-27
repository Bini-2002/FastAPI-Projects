from fastapi import FastAPI , Depends
from typing import Annotated
from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app.models import Todos

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


@app.get("/")
async def read_all(db: Annotated[Session, Depends(get_db)]):
    todos = db.query(Todos).all()
    return todos


