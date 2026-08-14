
from fastapi import APIRouter

from schemas.course_schema import (
    CourseCreate,
    CourseUpdate,
    CourseResponse
)

from services.course_services import (
    create_course,
    get_all_courses,
    get_course_by_id,
    update_course,
    delete_course
)

from services.selection_services import assign_professor_to_course


router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


@router.post("/", response_model=CourseResponse)
def create_course_api(course_data: CourseCreate):
    course = create_course(course_data)
    return course.to_dict()


@router.get("/", response_model=list[CourseResponse])
def get_all_courses_api():
    courses = get_all_courses()
    return [course.to_dict() for course in courses]


@router.get(
    "/{course_id}",
    response_model=CourseResponse
)
def get_course_by_id_api(course_id: str):
    course = get_course_by_id(course_id)
    return course.to_dict()


@router.put(
    "/{course_id}",
    response_model=CourseResponse
)
def update_course_api(
    course_id: str,
    course_data: CourseUpdate
):
    course = update_course(course_id, course_data)
    return course.to_dict()


@router.delete("/{course_id}")
def delete_course_api(course_id: str):
    delete_course(course_id)

    return {
        "message": "Course deleted successfully"
    }


@router.post("/{course_code}/professor/{personnel_code}")
def assign_professor_api(
    course_code: str,
    personnel_code: str
):
    assign_professor_to_course(
        personnel_code,
        course_code
    )

    return {
        "message": "Professor assigned to course successfully"
    }