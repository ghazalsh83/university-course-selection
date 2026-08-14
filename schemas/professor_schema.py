from pydantic import BaseModel, Field


class ProfessorCreate(BaseModel):
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    personnel_code: str = Field(min_length=3, max_length=20)
    department: str = Field(min_length=2, max_length=80)


class ProfessorUpdate(BaseModel):
    first_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=50
    )
    last_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=50
    )
    personnel_code: str | None = Field(
        default=None,
        min_length=3,
        max_length=20
    )
    department: str | None = Field(
        default=None,
        min_length=2,
        max_length=80
    )


class ProfessorResponse(BaseModel):
    ID: str
    first_name: str
    last_name: str
    personnel_code: str
    department: str
    courses: list