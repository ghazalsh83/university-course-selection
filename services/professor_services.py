from models.professor import Professor
from models.course import Course
from data.storage import load_all, save_all
from exceptions.custom_exceptions import (
    ProfessorNotFoundException,
    ProfessorAlreadyExistsException
)


def create_professor(professor_data):
    students, professors, courses = load_all()

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

    professor_courses = professor_data.get("courses", [])

    for course_code in professor_courses:
        for course_data in courses:

            if course_data["code"] == course_code:

                course = Course(
                    course_number=course_data["course_number"],
                    title=course_data["title"],
                    code=course_data["code"],
                    units=course_data["units"],
                    capacity=course_data["capacity"]
                )

                course.professor = professor

                for student in course_data.get("students", []):
                    course.students.append(student)

                professor.courses.append(course)

                break

    return professor


def get_all_professors():
    _, professors, courses = load_all()

    return [
        build_professor(
            professor_data,
            courses
        )
        for professor_data in professors
    ]


def get_professor_by_id(personnel_code):
    _, professors, courses = load_all()

    for professor_data in professors:

        if str(professor_data["personnel_code"]) == str(personnel_code):

            return build_professor(
                professor_data,
                courses
            )

    raise ProfessorNotFoundException(
        "Professor not found"
    )


def update_professor(personnel_code, professor_data):
    students, professors, courses = load_all()

    target_professor = None

    for professor in professors:

        if str(professor["personnel_code"]) == str(personnel_code):
            target_professor = professor
            break

    if target_professor is None:
        raise ProfessorNotFoundException(
            "Professor not found"
        )

    if professor_data.first_name is not None:
        target_professor["first_name"] = professor_data.first_name

    if professor_data.last_name is not None:
        target_professor["last_name"] = professor_data.last_name

    if professor_data.personnel_code is not None:

        for professor in professors:

            if (
                str(professor["personnel_code"])
                == str(professor_data.personnel_code)
                and str(professor["personnel_code"])
                != str(personnel_code)
            ):
                raise ProfessorAlreadyExistsException(
                    "Professor already exists"
                )

        target_professor["personnel_code"] = (
            professor_data.personnel_code
        )

    if professor_data.department is not None:
        target_professor["department"] = (
            professor_data.department
        )

    save_all(
        students,
        professors,
        courses
    )

    return build_professor(
        target_professor,
        courses
    )


def delete_professor(personnel_code):
    students, professors, courses = load_all()

    for i, professor in enumerate(professors):

        if str(professor["personnel_code"]) == str(personnel_code):

            deleted_professor = professors.pop(i)

            for course in courses:

                if str(course.get("professor")) == str(personnel_code):
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