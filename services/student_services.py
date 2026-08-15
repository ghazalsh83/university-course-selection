from models.student import Student
from schemas.student_schema import StudentCreate, StudentUpdate
from data.storage import load_all, save_all
from exceptions.custom_exceptions import (
    StudentNotFoundException,
    StudentAlreadyExistsException
)


def create_student(student_data: StudentCreate):
    students, professors, courses = load_all()

    for student in students:
        if student["student_number"] == student_data.student_number:
            raise StudentAlreadyExistsException("Student already exists")

    student = Student(
        ID=str(len(students) + 1),
        first_name=student_data.first_name,
        last_name=student_data.last_name,
        student_number=student_data.student_number,
        major=student_data.major
    )

    students.append(student.to_dict())
    save_all(students, professors, courses)

    return student


def get_all_students():
    students, _, _ = load_all()

    return [
        Student(
            ID=student["ID"],
            first_name=student["first_name"],
            last_name=student["last_name"],
            student_number=student["student_number"],
            major=student["major"],
            selected_courses=student.get("selected_courses", [])
        )
        for student in students
    ]


def get_student_by_id(student_number):
    students, _, _ = load_all()

    for student in students:
        if student["student_number"] == student_number:
            return Student(
                ID=student["ID"],
                first_name=student["first_name"],
                last_name=student["last_name"],
                student_number=student["student_number"],
                major=student["major"],
                selected_courses=student.get("selected_courses", [])
            )

    raise StudentNotFoundException("Student not found")


def update_student(student_number, student_data: StudentUpdate):
    students, professors, courses = load_all()

    target_student = None

    for student in students:
        if student["student_number"] == student_number:
            target_student = student
            break

    if target_student is None:
        raise StudentNotFoundException("Student not found")

    if student_data.student_number is not None:
        for student in students:
            if (
                student["student_number"] == student_data.student_number
                and student["student_number"] != student_number
            ):
                raise StudentAlreadyExistsException("Student already exists")

    if student_data.first_name is not None:
        target_student["first_name"] = student_data.first_name

    if student_data.last_name is not None:
        target_student["last_name"] = student_data.last_name

    if student_data.student_number is not None:
        target_student["student_number"] = student_data.student_number

    if student_data.major is not None:
        target_student["major"] = student_data.major

    save_all(students, professors, courses)

    return Student(
        ID=target_student["ID"],
        first_name=target_student["first_name"],
        last_name=target_student["last_name"],
        student_number=target_student["student_number"],
        major=target_student["major"],
        selected_courses=target_student.get("selected_courses", [])
    )


def delete_student(student_number):
    students, professors, courses = load_all()

    for i, student in enumerate(students):
        if student["student_number"] == student_number:
            deleted_student = students.pop(i)

            save_all(students, professors, courses)

            return deleted_student

    raise StudentNotFoundException("Student not found")