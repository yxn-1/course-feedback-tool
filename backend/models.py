from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)  # "student" or "instructor"
    enrollments = relationship("Enrollment", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    enrollments = relationship("Enrollment", back_populates="course")
    feedbacks = relationship("Feedback", back_populates="course")

class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

class Feedback(Base):
    __tablename__ = "feedbacks"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    content = Column(String)
    user = relationship("User", back_populates="feedbacks")
    course = relationship("Course", back_populates="feedbacks")

# SQLite setup
engine = create_engine("sqlite:///course_feedback.db")
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)