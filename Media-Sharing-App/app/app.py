from fastapi import FastAPI , HTTPException

app = FastAPI()

text_posts = {
    1 :{"title": "Hello World!", "content": "new post"},
    2 :{"title": "First Draft", "content": "initial idea"},
    3 :{"title": "Test Run 2.0", "content": "checking functionality"},
    4 :{"title": "Site Update", "content": "minor changes"},
    5 :{"title": "Blog Post 3", "content": "content placeholder"},
    6 :{"title": "Data Entry", "content": "sample record"},
    7 :{"title": "Quick Check", "content": "status confirmed"},
    8 :{"title": "Development Note", "content": "feature X added"},
    9 :{"title": "Announcement", "content": "coming soon"},
    10 :{"title": "Final Test", "content": "all systems go"},
}

@app.get("/posts")
def get_all_posts(limit: int = None):
    if limit:
        return dict(list(text_posts.items())[:limit])
    return text_posts

@app.get("/posts/{id}") #path parameter
def get_post(id: int):
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_posts.get(id)

