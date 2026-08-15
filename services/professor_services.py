from data.storage import load_all, save_all
from models.professor import Professor
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
        ID=str(len(professors) + 1),
        first_name=professor_data.first_name,
        last_name=professor_data.last_name,
        personnel_code=professor_data.personnel_code,
        department=professor_data.department
    )

    professors.append(professor.to_dict())

    save_all(students, professors, courses)

    return professor


def get_all_professors():
    students, professors, courses = load_all()

    result = []

    for professor_data in professors:
        professor = Professor(
            ID=professor_data["ID"],
            first_name=professor_data["first_name"],
            last_name=professor_data["last_name"],
            personnel_code=professor_data["personnel_code"],
            department=professor_data["department"]
        )

        for course_code in professor_data.get("courses", []):
            for course_data in courses:
                if course_data["code"] == course_code:
                    from services.course_services import build_course

                    course = build_course(course_data, professors, students)

                    if course.professor is None:
                        course.professor = professor

                    professor.courses.append(course)

                    break

        result.append(professor)

    return result


def get_professor_by_id(personnel_code):
    professors = get_all_professors()

    for professor in professors:
        if str(professor.personnel_code) == str(personnel_code):
            return professor

    raise ProfessorNotFoundException("Professor not found")


def update_professor(personnel_code, professor_data):
    students, professors, courses = load_all()

    target_professor = None

    for professor in professors:
        if str(professor["personnel_code"]) == str(personnel_code):
            target_professor = professor
            break

    if target_professor is None:
        raise ProfessorNotFoundException("Professor not found")

    if professor_data.personnel_code is not None:
        for professor in professors:
            if (
                professor["personnel_code"] == professor_data.personnel_code
                and professor["personnel_code"] != personnel_code
            ):
                raise ProfessorAlreadyExistsException(
                    "Professor already exists"
                )

    if professor_data.first_name is not None:
        target_professor["first_name"] = professor_data.first_name

    if professor_data.last_name is not None:
        target_professor["last_name"] = professor_data.last_name

    if professor_data.personnel_code is not None:
        target_professor["personnel_code"] = professor_data.personnel_code

    if professor_data.department is not None:
        target_professor["department"] = professor_data.department

    save_all(students, professors, courses)

    new_personnel_code = (
        professor_data.personnel_code
        if professor_data.personnel_code is not None
        else personnel_code
    )

    return get_professor_by_id(new_personnel_code)


def delete_professor(personnel_code):
    students, professors, courses = load_all()

    for i, professor in enumerate(professors):
        if str(professor["personnel_code"]) == str(personnel_code):
            professors.pop(i)

            save_all(students, professors, courses)

            return

    raise ProfessorNotFoundException("Professor not found")