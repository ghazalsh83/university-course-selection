from models.course import Course
from models.professor import Professor
from models.student import Student
from schemas.course_schema import CourseCreate, CourseUpdate
from data.storage import load_all, save_all
from exceptions.custom_exceptions import (
    CourseNotFoundException,
    CourseAlreadyExistsException
)


def create_course(course_data: CourseCreate):
    students, professors, courses = load_all()

    for course in courses:
        if course["code"] == course_data.code:
            raise CourseAlreadyExistsException("Course already exists")

    course = Course(
        course_number=len(courses) + 1,
        title=course_data.title,
        code=course_data.code,
        units=course_data.unit,
        capacity=course_data.capacity,
        major=course_data.major
    )

    courses.append(course.to_dict())
    save_all(students, professors, courses)

    return course


def build_course(course_data, professors, students):
    course = Course(
        course_number=course_data["course_number"],
        title=course_data["title"],
        code=course_data["code"],
        units=course_data["units"],
        capacity=course_data["capacity"],
        major=course_data.get("major")
    )

    professor_code = course_data.get("professor")

    if professor_code:
        for professor_data in professors:
            if professor_data["personnel_code"] == professor_code:
                professor = Professor(
                    ID=professor_data["ID"],
                    first_name=professor_data["first_name"],
                    last_name=professor_data["last_name"],
                    personnel_code=professor_data["personnel_code"],
                    department=professor_data["department"]
                )

                course.professor = professor
                break

    for student_number in course_data.get("students", []):
        for student_data in students:
            if student_data["student_number"] == student_number:
                student = Student(
                    ID=student_data["ID"],
                    first_name=student_data["first_name"],
                    last_name=student_data["last_name"],
                    student_number=student_data["student_number"],
                    major=student_data["major"]
                )

                course.students.append(student)
                break

    return course


def get_all_courses():
    students, professors, courses = load_all()

    return [
        build_course(course, professors, students)
        for course in courses
    ]


def get_course_by_id(course_code):
    students, professors, courses = load_all()

    for course_data in courses:
        if str(course_data["code"]) == str(course_code):
            return build_course(course_data, professors, students)

    raise CourseNotFoundException("Course not found")


def update_course(code, course_data: CourseUpdate):
    students, professors, courses = load_all()

    target_course = None

    for course in courses:
        if course["code"] == code:
            target_course = course
            break

    if target_course is None:
        raise CourseNotFoundException("Course not found")

    if course_data.code is not None:
        for course in courses:
            if (
                course["code"] == course_data.code
                and course["code"] != code
            ):
                raise CourseAlreadyExistsException("Course already exists")

    if course_data.major is not None:
        target_course["major"] = course_data.major

    if course_data.title is not None:
        target_course["title"] = course_data.title

    if course_data.code is not None:
        target_course["code"] = course_data.code

    if course_data.unit is not None:
        target_course["units"] = course_data.unit

    if course_data.capacity is not None:
        target_course["capacity"] = course_data.capacity

    save_all(students, professors, courses)

    return build_course(target_course, professors, students)


def delete_course(code):
    students, professors, courses = load_all()

    for i, course in enumerate(courses):
        if course["code"] == code:
            deleted_course = courses.pop(i)

            save_all(students, professors, courses)

            return deleted_course

    raise CourseNotFoundException("Course not found")