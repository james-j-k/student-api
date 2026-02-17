from pydantic import BaseModel
from typing import List, Optional

# For Student creation
class StudentCreate(BaseModel):
    name: str
    email: str

# For Course creation
class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None

# For Enrollment
class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int

# Response schemas
class CourseOut(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True

class StudentOut(BaseModel):
    id: int
    name: str
    email: str
    courses: List[CourseOut] = []

    class Config:
        from_attributes = True
