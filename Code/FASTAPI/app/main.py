from fastapi import FastAPI, HTTPException, status, Response, Depends
from pydantic import BaseModel, HttpUrl
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from sqlalchemy.orm import Session
from . database import engine, get_db



app = FastAPI()

models.Base.metadata.create_all(bind=engine)

#define request body schema
class Course(BaseModel):
    name: str
    instructor: str
    duration: float
    website: HttpUrl


while True:
    try:
        conn = psycopg2.connect(host = "localhost", database = "aiquest", user = "postgres", password="1234", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Successfully connected Datbase')
        break

    except Exception as error:
        print('Database connection failed')
        print("Error:",error)
        time.sleep(2)

@app.post("/post")
def create_post(post: Course):
    cursor.execute("""INSERT INTO course(name, instructor, duration, website) VALUES (%s,%s,%s,%s) RETURNING *""", (post.name, post.instructor, post.duration, str(post.website)))
    new_post = cursor.fetchone()
    conn.commit()
    return{"data": new_post}

@app.post('/courses')
def create_course(course:Course, db: Session = Depends(get_db)):
    new_course = models.Course(
        name = course.name,
        instructor = course.instructor,
        duration = course.duration,
        website = str(course.website)
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return {"Course": new_course}


@app.get("/course")
def studymart():
    return {"Course": "Django & Backend API development with Python"}

@app.get("/")
def aiquest():
    cursor.execute(""" SELECT * FROM course """)
    data = cursor.fetchall()
    return {"Data":data}

@app.get("/coursealchemy")
def course(db:Session = Depends(get_db)):
    course = db.query(models.Course).all()
    return {"Course": course}

@app.get("/django/api")
def django():
    return {"Type": "Basict to Advanced"}



@app.get("/course/{id}")
def get_course(id:int):
    cursor.execute(""" SELECT * FROM course WHERE id = %s """, (str(id),))
    course = cursor.fetchone()
    if not course:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail= f"Course with id:{id} was not found"
        )
    return{"Course_detail": course}

@app.get("/coursealchemy/{id}")
def aiquest_course(id:int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == id).first()
    if not course:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail= f"Course with id:{id} was not found"
        )
    return{"Course_detail": course}


@app.delete("/course/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(id: int):
    cursor.execute("""DELETE FROM course WHERE id = %s returning * """, ((str(id),)))
    deleted_course = cursor.fetchone()
    conn.commit()
    if deleted_course == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"course with id: {id} does not exist")
    return Response(status_code=status.HTTP_404_NOT_FOUND)

@app.put("/course/{id}")
def update_course(id: int, course: Course):
    cursor.execute("""UPDATE course SET name = %s, instructor = %s, duration = %s, website = %s WHERE id = %s RETURNING * """, (course.name, course.instructor, course.duration, str(course.website), str(id)))
    updated_course = cursor.fetchone()
    conn.commit()

    if updated_course == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"course with id: {id} does not exist")
    return{"data": updated_course}



    
    


