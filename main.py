from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()

class Post(BaseModel):
    title:str
    content:str
    

@app.get("/")
def root():
    return {"message":"Hello World"};

@app.get("/posts")
def get_posts():
    return {"title": "Instagram post", "content":"selfie"};

@app.post("/createpost")
def create_post(new_post:Post):
    print(new_post.title);
    return {"data":"new post"}
