from models.professor import Professor
from schemas.professor_schema import ProfessorCreate, ProfessorUpdate
from data.storage import load_all, save_all
from exceptions.custom_exceptions import (
    ProfessorNotFoundException,
    ProfessorAlreadyExistsException
)


def create_professor(professor_data: ProfessorCreate):
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
    _, professors, courses = load_all()

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
                    from models.course import Course

                    course = Course(
                        course_number=course_data["course_number"],
                        title=course_data["title"],
                        code=course_data["code"],
                        units=course_data["units"],
                        capacity=course_data["capacity"]
                    )

                    professor.assign_course(course)

        result.append(professor)

    return result


def get_professor_by_id(personnel_code):
    _, professors, courses = load_all()

    for professor_data in professors:
        if professor_data["personnel_code"] == personnel_code:

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
                        from models.course import Course

                        course = Course(
                            course_number=course_data["course_number"],
                            title=course_data["title"],
                            code=course_data["code"],
                            units=course_data["units"],
                            capacity=course_data["capacity"]
                        )

                        professor.assign_course(course)

            return professor

    raise ProfessorNotFoundException("Professor not found")


def update_professor(personnel_code, professor_data: ProfessorUpdate):
    students, professors, courses = load_all()

    target_professor = None

    for professor in professors:
        if professor["personnel_code"] == personnel_code:
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

    return get_professor_by_id(
        target_professor["personnel_code"]
    )


def delete_professor(personnel_code):
    students, professors, courses = load_all()

    for i, professor in enumerate(professors):
        if professor["personnel_code"] == personnel_code:
            deleted_professor = professors.pop(i)

            save_all(students, professors, courses)

            return deleted_professor

    raise ProfessorNotFoundException("Professor not found")