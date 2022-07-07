from fastapi import FastAPI, Response, status, HTTPException
from typing import Optional
from random import randrange
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {"title": "Title of post 1", "content": "Content of post 1", "id": 1},
    {"title": "Title of post 2", "content": "Content of post 2", "id": 2},
]


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post


def find_post_index(id):
    for idx, post in enumerate(my_posts):
        if post["id"] == id:
            return idx


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


# Default status code is provided in the decorator function
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)

    return {"data": post_dict}


# Any API with '/posts/some-string' route should be above this route otherwise the path will match with this route and string will be considered as ID
@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )

        # response.status_code=status.HTTP_404_NOT_FOUND;
        # return {"message":  f"Post with id {id} not found"};

    return {"data": post}


# When using `HTTP_204_NO_CONTENT` nothing can be returned in response
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_post_index(id)

    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )

    my_posts.pop(index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_post_index(id)

    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )

    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict

    return {"data": post}
