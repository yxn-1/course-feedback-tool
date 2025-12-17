from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Base, User, Course, Feedback, Enrollment, engine, SessionLocal

Base.metadata.create_all(bind=engine)  # create tables if not exists

app = FastAPI()

# Functions

def standarize_title(title: str) -> str:
    """standarize course title by removing spaces and converting to lowercase."""
    return title.replace(" ", "").lower()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.post("/users")
def create_user(name: str, role: str, db: Session = Depends(get_db)):
    user = User(name=name, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.post("/courses")
def create_course(title: str, instructor_id: int, db: Session = Depends(get_db)):
    instructor = db.query(User).filter_by(id=instructor_id, role="instructor").first()

    # Enforce only instructors can be assigned
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    if instructor.role != "instructor":
        raise HTTPException(status_code=400, detail=f"User {instructor.name} is not an instructor")
    
    course = Course(title=title, instructor_id=instructor.id)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

@app.get("/courses")
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    result = []
    for c in courses:
        result.append({
            "course": c.title,
            "instructor": c.instructor.name if c.instructor else "Instructor not assigned"
        })
    return result

@app.put("/courses/{course_id}/assign_instructor")
def assign_instructor(course_id: int, instructor_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).get(course_id)
    instructor = db.query(User).get(instructor_id)

    if not course or not instructor:
        raise HTTPException(status_code=404, detail="Course or instructor not found")
    if instructor.role != "instructor":
        raise HTTPException(status_code=400, detail="Only instructors can be assigned")
    
    course.instructor = instructor
    db.commit()
    db.refresh(course)
    return course


@app.get("/feedbacks")
def get_feedbacks(db: Session = Depends(get_db)):
    feedbacks = db.query(Feedback).all()
    result = []
    for f in feedbacks:
        result.append({
            "student": f.user.name if f.user else None,                                                             # Student name
            "course": f.course.title if f.course else "Course not found",                                           # Course title
            "professor": f.course.instructor.name if f.course and f.course.instructor else "Instructor not found",  # Instructor name
            "content": f.content                                                                                    # Feedback text
        })
    return result

# @app.post("/feedbacks")
# def create_feedback(user_id: int, course_id: int, content: str, db: Session = Depends(get_db)):
#     feedback = Feedback(user_id=user_id, course_id=course_id, content=content)
#     db.add(feedback)
#     db.commit()
#     db.refresh(feedback)
#     return feedback

@app.post("/feedbacks")
def add_feedback(student_name: str, course_title: str, content: str, db: Session = Depends(get_db)):
    # Look up student (case insensitive)
    student = db.query(User).filter(User.name.ilike(student_name), User.role == "student").first()
    if not student:
        raise HTTPException(status_code=404, detail=f"Student '{student_name}' not found")
    
    # Standarize name
    title = normalize_title(course_title)

   # Find course by standard title
    course = None
    for c in db.query(Course).all():
        if normalize_title(c.title) == title:
            course = c
            break

    if not course:
        raise HTTPException(status_code=404, detail=f"Course '{course_title}' not found")

    # Create feedback
    feedback = Feedback(user_id=student.id, course_id=course.id, content=content)
    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return {
        "student": student.name,
        "course": course.title,
        "professor": course.instructor.name if course.instructor else "Instructor not assigned",
        "content": feedback.content
    }
