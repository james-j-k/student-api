from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, get_db, Base

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Student Course Enrollment API")

# Create Student
@app.post("/students", response_model=schemas.StudentOut)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_student(db, student)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Create Course
@app.post("/courses", response_model=schemas.CourseCreate)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    return crud.create_course(db, course)

# Enroll Student
@app.post("/enrollments")
def enroll_student(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    try:
        return crud.enroll_student(db, enrollment)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get Student with Courses
@app.get("/students/{student_id}", response_model=schemas.StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    data = crud.get_student_courses(db, student_id)
    if not data:
        raise HTTPException(status_code=404, detail="Student not found")
    return data

