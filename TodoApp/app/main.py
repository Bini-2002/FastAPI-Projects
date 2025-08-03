from fastapi import FastAPI
from app.database import engine, Base, SessionLocal
from routers import auth , todos , admin

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router) # Include the auth router with a prefix
app.include_router(todos.router) # Include the todos router with a prefix
app.include_router(admin.router) # Include the admin router with a prefix

