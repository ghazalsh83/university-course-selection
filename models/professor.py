from .person import Person


class Professor(Person):
    def __init__(
        self,
        ID,
        first_name,
        last_name,
        personnel_code,
        department
    ):
        super().__init__(ID, first_name, last_name)

        self.personnel_code = personnel_code
        self.department = department
        self.courses = []

    def assign_course(self, course):
        self.courses.append(course)

    def get_courses(self):
        return self.courses

    def to_dict(self):
        return {
            "ID": self.ID,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "personnel_code": self.personnel_code,
            "department": self.department,
            "courses": [course.to_dict() for course in self.courses]
        }