from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl


app = FastAPI()

#define request body schema
class Course(BaseModel):
    name: str
    instructor: str
    duration: float
    website: HttpUrl

@app.post("/post")
def create_post(post: Course):
    return{"data": post}


@app.get("/course")
def studymart():
    return {"Course": "Django & Backend API development with Python"}

@app.get("/")
def aiquest():
    return {"Django":"API"}

@app.get("/django/api")
def django():
    return {"Type": "Basict to Advanced"}

