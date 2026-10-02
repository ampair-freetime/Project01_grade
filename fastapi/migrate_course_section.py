"""Add the optional course section default. Run: python migrate_course_section.py."""

from sqlalchemy import text
from app.db import engine


def migrate_course_section():
    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE courses ADD COLUMN IF NOT EXISTS section VARCHAR(50)"))
    print("Course section column is ready")


if __name__ == "__main__":
    migrate_course_section()
