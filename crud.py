from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models, schemas

# Students
def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(name=student.name, email=student.email)
    db.add(db_student)
    try:
        db.commit()
        db.refresh(db_student)
        return db_student
    except IntegrityError:
        db.rollback()
        raise ValueError("Email already exists")

def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

# Courses
def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(title=course.title, description=course.description)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def get_course(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.id == course_id).first()

# Enrollments
def enroll_student(db: Session, enrollment: schemas.EnrollmentCreate):
    # Check if student exists
    student = get_student(db, enrollment.student_id)
    if not student:
        raise ValueError("Student does not exist")
    # Check if course exists
    course = get_course(db, enrollment.course_id)
    if not course:
        raise ValueError("Course does not exist")
    # Add enrollment
    db_enroll = models.Enrollment(student_id=enrollment.student_id, course_id=enrollment.course_id)
    db.add(db_enroll)
    try:
        db.commit()
        db.refresh(db_enroll)
        return db_enroll
    except IntegrityError:
        db.rollback()
        raise ValueError("Student already enrolled in this course")

def get_student_courses(db: Session, student_id: int):
    student = get_student(db, student_id)
    if not student:
        return None
    courses = db.query(models.Course).join(models.Enrollment)\
                .filter(models.Enrollment.student_id == student_id).all()
    return {"id": student.id, "name": student.name, "email": student.email, "courses": courses}
