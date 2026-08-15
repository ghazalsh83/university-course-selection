from models.professor import Professor
from data.storage import load_all, save_all
from exceptions.custom_exceptions import (
    ProfessorNotFoundException,
    ProfessorAlreadyExistsException
)


def create_professor(professor_data):
    students, professors, courses = load_all()

    # بررسی تکراری نبودن استاد
    for professor in professors:
        if professor["personnel_code"] == professor_data.personnel_code:
            raise ProfessorAlreadyExistsException(
                "Professor already exists"
            )

    professor = Professor(
        ID=professor_data.ID,
        first_name=professor_data.first_name,
        last_name=professor_data.last_name,
        personnel_code=professor_data.personnel_code,
        department=professor_data.department
    )

    professors.append(professor.to_dict())

    save_all(
        students,
        professors,
        courses
    )

    return professor


def build_professor(professor_data, courses):
    professor = Professor(
        ID=professor_data["ID"],
        first_name=professor_data["first_name"],
        last_name=professor_data["last_name"],
        personnel_code=professor_data["personnel_code"],
        department=professor_data["department"]
    )

    # پیدا کردن درس‌های استاد
    for course_code in professor_data.get("courses", []):
        for course_data in courses:
            if course_data["code"] == course_code:
                professor.courses.append(
                    course_data
                )
                break

    return professor


def get_all_professors():
    _, professors, courses = load_all()

    return [
        build_professor(
            professor,
            courses
        )
        for professor in professors
    ]


def get_professor_by_id(personnel_code):
    _, professors, courses = load_all()

    for professor_data in professors:
        if (
            str(professor_data["personnel_code"])
            == str(personnel_code)
        ):
            return build_professor(
                professor_data,
                courses
            )

    raise ProfessorNotFoundException(
        "Professor not found"
    )


def delete_professor(personnel_code):
    students, professors, courses = load_all()

    for i, professor in enumerate(professors):

        if (
            str(professor["personnel_code"])
            == str(personnel_code)
        ):

            deleted_professor = professors.pop(i)

            # حذف ارتباط استاد از درس‌ها
            for course in courses:
                if course.get("professor") == personnel_code:
                    course["professor"] = None

            save_all(
                students,
                professors,
                courses
            )

            return deleted_professor

    raise ProfessorNotFoundException(
        "Professor not found"
    )