# test_db.py
from models import Base, engine, SessionLocal, User, Course, Enrollment, Feedback

# --- Reset database ---
Base.metadata.drop_all(bind=engine)  # remove old tables
Base.metadata.create_all(bind=engine)  # create new tables

db = SessionLocal()

# --- Create Users ---
instructors = [
    User(name="Dr. Smith", role="instructor"),
    User(name="Dr. Johnson", role="instructor")
]

students = [
    User(name="Alice", role="student"),
    User(name="Bob", role="student"),
    User(name="Charlie", role="student")
]

db.add_all(instructors + students)
db.commit()

# --- Create Courses and assign instructors ---
courses = [
    Course(title="CPSC 110", instructor_id=instructors[0].id),
    Course(title="CPSC 210", instructor_id=instructors[1].id),
    Course(title="MATH 100", instructor_id=instructors[0].id)
]

# Enforce only instructors can be assigned
for c in courses:
    instructor = db.query(User).filter_by(id=c.instructor_id).first()
    if instructor.role != "instructor":
        raise ValueError(f"Cannot assign {instructor.name} as instructor; not an instructor!")

db.add_all(courses)
db.commit()

# --- Create Enrollments ---
enrollments = [
    Enrollment(user_id=students[0].id, course_id=courses[0].id),
    Enrollment(user_id=students[1].id, course_id=courses[0].id),
    Enrollment(user_id=students[2].id, course_id=courses[1].id),
    Enrollment(user_id=students[0].id, course_id=courses[2].id),
    Enrollment(user_id=students[1].id, course_id=courses[2].id)
]

db.add_all(enrollments)
db.commit()

# --- Create Feedback ---
feedbacks = [
    Feedback(user_id=students[0].id, course_id=courses[0].id, content="Great lecture!"),
    Feedback(user_id=students[1].id, course_id=courses[0].id, content="Loved the examples."),
    Feedback(user_id=students[2].id, course_id=courses[1].id, content="Challenging but fun."),
    Feedback(user_id=students[0].id, course_id=courses[2].id, content="Could use more practice problems."),
    Feedback(user_id=students[1].id, course_id=courses[2].id, content="Helpful exercises!")
]

db.add_all(feedbacks)
db.commit()

# --- Print Test Data ---
print("\n--- Users ---")
for u in db.query(User).all():
    print(f"{u.id}: {u.name} ({u.role})")

print("\n--- Courses with Instructors ---")
for c in db.query(Course).all():
    print(f"{c.id}: {c.title} - Instructor: {c.instructor.name}")

print("\n--- Enrollments ---")
for e in db.query(Enrollment).all():
    print(f"Student: {e.user.name} -> Course: {e.course.title}")

print("\n--- Feedback ---")
for f in db.query(Feedback).all():
    print(f"{f.user.name} on {f.course.title}: {f.content}")

db.close()