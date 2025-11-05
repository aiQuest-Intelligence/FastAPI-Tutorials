from pydantic import BaseModel, HttpUrl

#define request body schema
class CourseCreate(BaseModel):
    name: str
    instructor: str
    duration: float
    website: HttpUrl

class CourseResponse(CourseCreate):
    id : int

    class Config:
        orm_model = True
# class CourseResponse(BaseModel):
#     name: str
#     instructor: str