from pydantic import BaseModel, Field


class CourseCreate(BaseModel):
    major: str = Field(min_length=2, max_length=80)
    title: str = Field(min_length=2, max_length=100)
    code: str = Field(min_length=2, max_length=20)
    unit: int = Field(ge=1, le=5)
    capacity: int = Field(ge=1, le=200)


class CourseUpdate(BaseModel):
    major: str | None = Field(
        default=None,
        min_length=2,
        max_length=80
    )
    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    code: str | None = Field(
        default=None,
        min_length=2,
        max_length=20
    )
    unit: int | None = Field(
        default=None,
        ge=1,
        le=5
    )
    capacity: int | None = Field(
        default=None,
        ge=1,
        le=200
    )


class CourseResponse(BaseModel):
    course_number: int
    title: str
    code: str
    units: int
    capacity: int
    professor: str | None
    students: list[str]