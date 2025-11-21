from fastapi import FastAPI , HTTPException

app = FastAPI()

text_posts = {
  1: {"title": "Hello World!", "content": "new post"},}

@app.get("/posts")
def get_posts():
    return text_posts

@app.get("/posts/{id}") #path parameter
def get_post(id: int):
    return text_posts.get(id)
