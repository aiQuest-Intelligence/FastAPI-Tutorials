from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from .. database import get_db
from typing import List
from .. import oauth2

router = APIRouter(
    prefix="/course",
    tags = ['Course']
)

@router.post('/', response_model=schemas.CourseResponse)
def create_course(course:schemas.CourseCreate, db: Session = Depends(get_db), get_current_user: int=Depends(oauth2.get_current_user)):
    new_course = models.Course(**course.model_dump())
    new_course.website = str(course.website)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course



@router.get("/", response_model= List[schemas.CourseResponse])
def course(db:Session = Depends(get_db), get_current_user: int=Depends(oauth2.get_current_user)):
    courses = db.query(models.Course).all()
    return courses



@router.get("/{id}", response_model=schemas.CourseResponse)
def aiquest_course(id:int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == id).first()
    if not course:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail= f"Course with id:{id} was not found"
        )
    return course




@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_aiquest_course(id:int, db:Session=Depends(get_db)):
    course_query = db.query(models.Course).filter(models.Course.id==id)
    course = course_query.first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"course with id: {id} does not exist")
    course_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)




@router.put("/{id}", response_model=schemas.CourseResponse)
def update_aiquest_course(id:int, updated_course: schemas.CourseCreate, db:Session=Depends(get_db)):
    course_query = db.query(models.Course).filter(models.Course.id==id)
    course = course_query.first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"course with id: {id} does not exist")
    update_data = updated_course.model_dump()
    update_data["website"] = str(update_data["website"])
    course_query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(course)
    return course
