from .person import Person


class Student(Person):
    def __init__(
        self,
        ID,
        first_name,
        last_name,
        student_number,
        major,
        selected_courses=None
    ):
        super().__init__(ID, first_name, last_name)

        self.student_number = student_number
        self.major = major
        self.selected_courses = (
            selected_courses if selected_courses is not None else []
        )

    def select_course(self, course_code):
        self.selected_courses.append(course_code)

    def drop_course(self, course_code):
        if course_code in self.selected_courses:
            self.selected_courses.remove(course_code)

    def get_courses(self):
        return self.selected_courses

    def to_dict(self):
        return {
            "ID": self.ID,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "student_number": self.student_number,
            "major": self.major,
            "selected_courses": self.selected_courses
        }