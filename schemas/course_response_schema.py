from pydantic import BaseModel


class CourseResponse(BaseModel):
    course_number: int
    title: str
    code: str
    units: int
    capacity: int
    professor: str | None
    students: list