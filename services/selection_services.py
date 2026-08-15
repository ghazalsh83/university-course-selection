from data.storage import load_all, save_all
from exceptions.custom_exceptions import (
    StudentNotFoundException,
    CourseNotFoundException,
    CourseFullException,
    StudentAlreadySelectedException,
    StudentHasNotSelectedCourseException,
    ProfessorNotFoundException
)
from services.course_services import build_course


def select_course_for_student(student_number, course_code):
    students, professors, courses = load_all()

    student_data = None
    course_data = None

    # پیدا کردن دانشجو
    for student in students:
        if student["student_number"] == student_number:
            student_data = student
            break

    if student_data is None:
        raise StudentNotFoundException("Student not found")

    # پیدا کردن درس
    for course in courses:
        if course["code"] == course_code:
            course_data = course
            break

    if course_data is None:
        raise CourseNotFoundException("Course not found")

    # بررسی انتخاب قبلی درس
    if course_code in student_data["selected_courses"]:
        raise StudentAlreadySelectedException(
            "Student already selected this course"
        )

    # بررسی ظرفیت درس
    if len(course_data["students"]) >= course_data["capacity"]:
        raise CourseFullException("Course is full")

    # اضافه کردن درس برای دانشجو
    course_data["students"].append(student_number)
    student_data["selected_courses"].append(course_code)

    save_all(students, professors, courses)

    return True


def drop_course_for_student(student_number, course_code):
    students, professors, courses = load_all()

    student_data = None
    course_data = None

    # پیدا کردن دانشجو
    for student in students:
        if student["student_number"] == student_number:
            student_data = student
            break

    if student_data is None:
        raise StudentNotFoundException("Student not found")

    # پیدا کردن درس
    for course in courses:
        if course["code"] == course_code:
            course_data = course
            break

    if course_data is None:
        raise CourseNotFoundException("Course not found")

    # بررسی اینکه دانشجو این درس را گرفته یا نه
    if course_code not in student_data["selected_courses"]:
        raise StudentHasNotSelectedCourseException(
            "Student has not selected this course"
        )

    # حذف درس از لیست دانشجو
    student_data["selected_courses"].remove(course_code)

    # حذف دانشجو از لیست دانشجویان درس
    if student_number in course_data["students"]:
        course_data["students"].remove(student_number)

    save_all(students, professors, courses)

    return True


def get_student_courses(student_number):
    students, professors, courses = load_all()

    student_data = None

    # پیدا کردن دانشجو
    for student in students:
        if student["student_number"] == student_number:
            student_data = student
            break

    if student_data is None:
        raise StudentNotFoundException("Student not found")

    result = []

    # پیدا کردن اطلاعات کامل درس‌های انتخاب شده
    for course_code in student_data["selected_courses"]:
        for course_data in courses:
            if course_data["code"] == course_code:

                course = build_course(
                    course_data,
                    professors,
                    students
                )

                result.append(course)

                break

    return result


def assign_professor_to_course(
    personnel_code,
    course_code
):
    students, professors, courses = load_all()

    professor_data = None
    course_data = None

    # پیدا کردن استاد
    for professor in professors:
        if professor["personnel_code"] == personnel_code:
            professor_data = professor
            break

    if professor_data is None:
        raise ProfessorNotFoundException("Professor not found")

    # پیدا کردن درس
    for course in courses:
        if course["code"] == course_code:
            course_data = course
            break

    if course_data is None:
        raise CourseNotFoundException("Course not found")

    # تخصیص استاد به درس
    course_data["professor"] = personnel_code

    # اضافه کردن درس به لیست دروس استاد
    if "courses" not in professor_data:
        professor_data["courses"] = []

    if course_code not in professor_data["courses"]:
        professor_data["courses"].append(course_code)

    save_all(
        students,
        professors,
        courses
    )

    return True