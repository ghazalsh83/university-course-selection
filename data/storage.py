import json
import os


DATA_DIR = os.path.dirname(__file__)

STUDENTS_FILE = os.path.join(DATA_DIR, "students.json")
PROFESSORS_FILE = os.path.join(DATA_DIR, "professors.json")
COURSES_FILE = os.path.join(DATA_DIR, "courses.json")


student_counter = 1
professor_counter = 1
course_counter = 1


def _read_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def _write_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def save_all(students, professors, courses):
    _write_json(STUDENTS_FILE, students)
    _write_json(PROFESSORS_FILE, professors)
    _write_json(COURSES_FILE, courses)


def load_all():
    students = _read_json(STUDENTS_FILE)
    professors = _read_json(PROFESSORS_FILE)
    courses = _read_json(COURSES_FILE)

    return students, professors, courses


def reset_storage():
    _write_json(STUDENTS_FILE, [])
    _write_json(PROFESSORS_FILE, [])
    _write_json(COURSES_FILE, [])