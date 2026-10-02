"""Move legacy score sections to enrollments, then remove scores.section.

Run from fastapi/: python migrate_score_section.py
Stop application workers while running this PostgreSQL migration.
Existing enrollment sections take precedence; missing sections use the latest
nonblank legacy score section. The migration is safe to run again.
"""

from sqlalchemy import inspect, text
from app.db import engine
from migrate_enrollment import migrate_enrollment


def migrate_score_section():
    # Also backfill enrollments for legacy scores that do not have a roster row.
    migrate_enrollment()

    with engine.begin() as conn:
        if not any(
            column["name"] == "section" for column in inspect(conn).get_columns("scores")
        ):
            print("scores.section is already removed")
            return

        # Prevent uploads from changing sections between backfill and column removal.
        conn.execute(text("LOCK TABLE scores, enrollments IN ACCESS EXCLUSIVE MODE"))
        result = conn.execute(text("""
            WITH latest_sections AS (
                SELECT DISTINCT ON (s.student_id, q.course_code)
                       s.student_id, q.course_code, btrim(s.section) AS section
                FROM scores s
                JOIN quizzes q ON q.quiz_id = s.quiz_id
                WHERE NULLIF(btrim(s.section), '') IS NOT NULL
                ORDER BY s.student_id, q.course_code,
                         s.updated_at DESC NULLS LAST, s.score_id DESC
            )
            UPDATE enrollments e
            SET section = latest.section
            FROM latest_sections latest
            WHERE e.student_id = latest.student_id
              AND e.course_code = latest.course_code
              AND NULLIF(btrim(e.section), '') IS NULL
        """))
        conn.execute(text("ALTER TABLE scores DROP COLUMN section"))
        print(f"Backfilled enrollment sections: {result.rowcount}")
        print("Removed scores.section")


if __name__ == "__main__":
    migrate_score_section()
