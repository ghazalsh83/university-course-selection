from pydantic import BaseModel


class StudentResponse(BaseModel):
    ID: str
    first_name: str
    last_name: str
    student_number: str
    major: str
    selected_courses: list