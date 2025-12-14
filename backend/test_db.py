from models import SessionLocal, User, Course, Enrollment, Feedback

db = SessionLocal()

# Add sample data
instructor = User(name="Dr. Smith", role="instructor")
student = User(name="Alice", role="student")
course = Course(title="CPSC 110")
db.add_all([instructor, student, course])
db.commit()

# Enroll student
enrollment = Enrollment(user_id=student.id, course_id=course.id)
db.add(enrollment)
db.commit()

# Add feedback
fb = Feedback(user_id=student.id, course_id=course.id, content="Great lecture!")
db.add(fb)
db.commit()

# Query feedback
for feedback in db.query(Feedback).all():
    print(feedback.content)