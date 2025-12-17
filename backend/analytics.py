from sqlalchemy import text
from database import SessionLocal


def feedback_per_course():
    db = SessionLocal()

    # How many feedback per course
    query = text(
        """
        SELECT
            c.title as course,
            COUNT(f.id) AS feedback_count
        FROM courses c
        LEFT JOIN feedbacks f ON c.id = f.course_id
        GROUP BY c.id
        ORDER BY feedback_count DESC;
    """
    )

    results = db.execute(query).fetchall()

    print("\nNumber of feedback per course:")
    for r in results:
        print(r)

    db.close()


def feedback_per_user():

    db = SessionLocal()

    # How many feedbacks per user give
    query = text(
        """
        SELECT
            u.name,
            u.role,
            COUNT(f.id) as fcount
        FROM feedbacks f
        JOIN users u on f.user_id = u.id
        GROUP by u.id, u.name, u.role
        ORDER by fcount DESC;
    """
    )

    results = db.execute(query).fetchall()

    print("\nHow many feedback did each student give:")
    for r in results:
        print(r)

    db.close()


if __name__ == "__main__":
    feedback_per_course()
    feedback_per_user()
