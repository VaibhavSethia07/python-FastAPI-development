from fastapi import FastAPI
from typing import Optional
from random import randrange
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    id: int


my_posts = [
    {"title": "Title of post 1", "content": "Content of post 1", "id": 1},
    {"title": "Title of post 2", "content": "Content of post 2", "id": 2},
]

def find_post(id):
    for post in my_posts:
        if post['id']==id:
            return post;


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts")
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)

    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id:int):
    post=find_post(id);

    return {"data": post}
