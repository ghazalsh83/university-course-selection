
from fastapi import APIRouter

from schemas.professor_schema import (
    ProfessorCreate,
    ProfessorUpdate,
    ProfessorResponse
)

from schemas.course_schema import CourseResponse

from services.professor_services import (
    create_professor,
    get_all_professors,
    get_professor_by_id,
    update_professor,
    delete_professor
)


router = APIRouter(
    prefix="/professors",
    tags=["Professors"]
)


@router.post("/", response_model=ProfessorResponse)
def create_professor_api(professor_data: ProfessorCreate):
    professor = create_professor(professor_data)
    return professor.to_dict()


@router.get("/", response_model=list[ProfessorResponse])
def get_all_professors_api():
    professors = get_all_professors()
    return [professor.to_dict() for professor in professors]


@router.get(
    "/{personnel_code}",
    response_model=ProfessorResponse
)
def get_professor_api(personnel_code: str):
    professor = get_professor_by_id(personnel_code)
    return professor.to_dict()


@router.put(
    "/{personnel_code}",
    response_model=ProfessorResponse
)
def update_professor_api(
    personnel_code: str,
    professor_data: ProfessorUpdate
):
    professor = update_professor(
        personnel_code,
        professor_data
    )

    return professor.to_dict()


@router.delete("/{personnel_code}")
def delete_professor_api(personnel_code: str):
    delete_professor(personnel_code)

    return {
        "message": "Professor deleted successfully"
    }