from pydantic import BaseModel


class ProfessorResponse(BaseModel):
    ID: str
    first_name: str
    last_name: str
    personnel_code: str
    department: str
    courses: list