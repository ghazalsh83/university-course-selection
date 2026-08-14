class CourseSelectionException(Exception):
    pass


class StudentNotFoundException(CourseSelectionException):
    pass


class StudentAlreadyExistsException(CourseSelectionException):
    pass


class ProfessorNotFoundException(CourseSelectionException):
    pass


class ProfessorAlreadyExistsException(CourseSelectionException):
    pass


class CourseNotFoundException(CourseSelectionException):
    pass


class CourseAlreadyExistsException(CourseSelectionException):
    pass


class CourseFullException(CourseSelectionException):
    pass


class StudentAlreadySelectedException(CourseSelectionException):
    pass


class StudentHasNotSelectedCourseException(CourseSelectionException):
    pass