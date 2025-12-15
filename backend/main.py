from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Base, User, Course, Feedback, Enrollment, engine, SessionLocal

Base.metadata.create_all(bind=engine)  # create tables if not exists

app = FastAPI()

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

@app.get("/courses")
def read_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

@app.post("/courses")
def create_course(title: str, instructor_id: int, db: Session = Depends(get_db)):
    instructor = db.query(User).filter_by(id=instructor_id, role="instructor").first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    course = Course(title=title, instructor_id=instructor.id)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

@app.get("/courses_with_instructors")
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    result = []
    for c in courses:
        result.append({
            "course": c.title,
            "instructor": c.instructor.name if c.instructor else None
        })
    return result

@app.get("/feedbacks")
def read_feedbacks(db: Session = Depends(get_db)):
    return db.query(Feedback).all()

@app.post("/feedbacks")
def create_feedback(user_id: int, course_id: int, content: str, db: Session = Depends(get_db)):
    feedback = Feedback(user_id=user_id, course_id=course_id, content=content)
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback