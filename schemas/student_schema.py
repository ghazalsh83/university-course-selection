from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    student_number: str = Field(min_length=3, max_length=20)
    major: str = Field(min_length=2, max_length=80)


class StudentUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=2, max_length=50)
    last_name: str | None = Field(default=None, min_length=2, max_length=50)
    student_number: str | None = Field(default=None, min_length=3, max_length=20)
    major: str | None = Field(default=None, min_length=2, max_length=80)

class StudentResponse(BaseModel):
    ID: str
    first_name: str
    last_name: str
    student_number: str
    major: str
    selected_courses: list[str]