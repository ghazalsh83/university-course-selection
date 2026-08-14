from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from routers.students import router as students_router
from routers.professors import router as professors_router
from routers.courses import router as courses_router

from data.storage import load_all, save_all

from exceptions.custom_exceptions import (
    StudentNotFoundException,
    StudentAlreadyExistsException,
    ProfessorNotFoundException,
    ProfessorAlreadyExistsException,
    CourseNotFoundException,
    CourseAlreadyExistsException,
    CourseFullException,
    StudentAlreadySelectedException,
    StudentHasNotSelectedCourseException,
)


app = FastAPI(
    title="University Course Selection System"
)


app.include_router(students_router)
app.include_router(professors_router)
app.include_router(courses_router)


@app.on_event("startup")
def startup_event():
    load_all()


@app.on_event("shutdown")
def shutdown_event():
    students, professors, courses = load_all()
    save_all(students, professors, courses)


@app.get("/")
def root():
    return {
        "message": "University Course Selection System"
    }


@app.get("/summary")
def get_summary():
    students, professors, courses = load_all()

    return {
        "students_count": len(students),
        "professors_count": len(professors),
        "courses_count": len(courses)
    }


@app.get("/all-data")
def get_all_data():
    students, professors, courses = load_all()

    return {
        "students": students,
        "professors": professors,
        "courses": courses
    }


@app.exception_handler(StudentNotFoundException)
async def student_not_found_handler(
    request: Request,
    exc: StudentNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )


@app.exception_handler(StudentAlreadyExistsException)
async def student_already_exists_handler(
    request: Request,
    exc: StudentAlreadyExistsException
):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)}
    )


@app.exception_handler(ProfessorNotFoundException)
async def professor_not_found_handler(
    request: Request,
    exc: ProfessorNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )


@app.exception_handler(ProfessorAlreadyExistsException)
async def professor_already_exists_handler(
    request: Request,
    exc: ProfessorAlreadyExistsException
):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)}
    )


@app.exception_handler(CourseNotFoundException)
async def course_not_found_handler(
    request: Request,
    exc: CourseNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )


@app.exception_handler(CourseAlreadyExistsException)
async def course_already_exists_handler(
    request: Request,
    exc: CourseAlreadyExistsException
):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)}
    )


@app.exception_handler(CourseFullException)
async def course_full_handler(
    request: Request,
    exc: CourseFullException
):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )


@app.exception_handler(StudentAlreadySelectedException)
async def student_already_selected_handler(
    request: Request,
    exc: StudentAlreadySelectedException
):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)}
    )


@app.exception_handler(StudentHasNotSelectedCourseException)
async def student_has_not_selected_course_handler(
    request: Request,
    exc: StudentHasNotSelectedCourseException
):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )