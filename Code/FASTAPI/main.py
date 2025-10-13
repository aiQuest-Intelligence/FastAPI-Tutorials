from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
import psycopg2
from psycopg2.extras import RealDictCursor
import time



app = FastAPI()

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


@app.get("/course")
def studymart():
    return {"Course": "Django & Backend API development with Python"}

@app.get("/")
def aiquest():
    cursor.execute(""" SELECT * FROM course """)
    data = cursor.fetchall()
    return {"Data":data}

@app.get("/django/api")
def django():
    return {"Type": "Basict to Advanced"}

