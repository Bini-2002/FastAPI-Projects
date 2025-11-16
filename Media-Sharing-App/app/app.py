from fastapi import FastAPI

hi = FastAPI()

@hi.get("/")
def read_root():
    return {"Hello": "World"} #JSON response with a greeting

