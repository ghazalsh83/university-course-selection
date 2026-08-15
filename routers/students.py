from fastapi import APIRouter, Query

from schemas.student_schema import (
    StudentCreate,
    StudentUpdate,
    StudentResponse
)

from schemas.course_schema import CourseResponse

from services.student_services import (
    create_student,
    get_all_students,
    get_student_by_id,
    update_student,
    delete_student
)

from services.selection_services import (
    get_student_courses,
    select_course_for_student,
    drop_course_for_student
)


router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.post("/", response_model=StudentResponse)
def create_student_api(student_data: StudentCreate):
    student = create_student(student_data)
    return student.to_dict()


@router.get("/", response_model=list[StudentResponse])
def get_all_students_api():
    students = get_all_students()
    return [student.to_dict() for student in students]


@router.get("/search")
def search_students(
    major: str = Query(..., min_length=2)
):
    students = get_all_students()

    return [
        student.to_dict()
        for student in students
        if major.lower() in student.major.lower()
    ]


@router.get("/{student_id}", response_model=StudentResponse)
def get_student_api(student_id: str):
    student = get_student_by_id(student_id)
    return student.to_dict()


@router.put("/{student_id}", response_model=StudentResponse)
def update_student_api(
    student_id: str,
    student_data: StudentUpdate
):
    student = update_student(student_id, student_data)
    return student.to_dict()


@router.delete("/{student_id}")
def delete_student_api(student_id: str):
    delete_student(student_id)

    return {
        "message": "دانشجو با موفقیت حذف شد."
    }


@router.get(
    "/{student_id}/courses",
    response_model=list[CourseResponse]
)
def get_student_courses_api(student_id: str):
    courses = get_student_courses(student_id)
    return [course.to_dict() for course in courses]


@router.post("/{student_id}/courses/{course_code}")
def select_course_api(
    student_id: str,
    course_code: str
):
    select_course_for_student(
        student_id,
        course_code
    )

    return {
        "message": "درس با موفقیت برای دانشجو انتخاب شد."
    }


@router.delete("/{student_id}/courses/{course_code}")
def drop_course_api(
    student_id: str,
    course_code: str
):
    drop_course_for_student(
        student_id,
        course_code
    )

    return {
        "message": "درس با موفقیت از لیست دانشجو حذف شد."
    }