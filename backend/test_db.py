from models import SessionLocal, User, Course, Enrollment, Feedback

db = SessionLocal()

# Clear previous data (optional, useful for re-runs)
db.query(Feedback).delete()
db.query(Enrollment).delete()
db.query(User).delete()
db.query(Course).delete()
db.commit()

# --- Users ---
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

# --- Courses ---
courses = [
    Course(title="CPSC 110"),
    Course(title="CPSC 210"),
    Course(title="MATH 100")
]
db.add_all(courses)
db.commit()

# --- Enrollments ---
enrollments = [
    Enrollment(user_id=students[0].id, course_id=courses[0].id),
    Enrollment(user_id=students[1].id, course_id=courses[0].id),
    Enrollment(user_id=students[2].id, course_id=courses[1].id),
    Enrollment(user_id=students[0].id, course_id=courses[2].id)
]
db.add_all(enrollments)
db.commit()

# --- Feedback ---
feedbacks = [
    Feedback(user_id=students[0].id, course_id=courses[0].id, content="Great lecture!"),
    Feedback(user_id=students[1].id, course_id=courses[0].id, content="Loved the examples."),
    Feedback(user_id=students[2].id, course_id=courses[1].id, content="Challenging but fun."),
    Feedback(user_id=students[0].id, course_id=courses[2].id, content="Could use more practice problems.")
]
db.add_all(feedbacks)
db.commit()

# --- Test Query ---
print("All feedbacks:")
for fb in db.query(Feedback).all():
    print(f"{fb.user.name} on {fb.course.title}: {fb.content}")
