class Course:
    def __init__(
        self,
        course_number,
        title,
        code,
        units,
        capacity,
        major=None
    ):
        self.course_number = course_number
        self.title = title
        self.code = code
        self.units = units
        self.capacity = capacity
        self.major = major
        self.professor = None
        self.students = []

    def is_full(self):
        return len(self.students) >= self.capacity

    def add_student(self, student):
        if not self.is_full():
            self.students.append(student)

    def remove_student(self, student):
        if student in self.students:
            self.students.remove(student)

    def assign_professor(self, professor):
        self.professor = professor
        professor.assign_course(self)

    def to_dict(self):
        return {
            "course_number": self.course_number,
            "title": self.title,
            "code": self.code,
            "units": self.units,
            "capacity": self.capacity,
            "major": self.major,
            "professor": (
                self.professor.get_full_name()
                if self.professor
                else None
            ),
            "students": [
                student.get_full_name()
                for student in self.students
            ]
        }