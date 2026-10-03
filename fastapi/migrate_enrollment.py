# fastapi/migrate_enrollment.py
# Phase 1 — Student Self-Enrollment: สร้างตาราง enrollments + join_code ของ courses + backfill
# รันซ้ำได้ (idempotent): python migrate_enrollment.py
# ใช้ได้กับ PostgreSQL เท่านั้น (ทั้งโปรเจกต์ใช้ gen_random_uuid() อยู่แล้ว)
from sqlalchemy import inspect, text
from app.db import Base, SessionLocal, engine
from app.models import Course
from app.join_code import generate_join_code
from migrate_legacy_schema import migrate_legacy_schema


def migrate_enrollment():
    # Existing Docker volumes may still contain the original integer-ID schema.
    migrate_legacy_schema(engine)
    # 1. สร้างตารางที่ยังไม่มี (DB ใหม่ = ทุกตาราง, DB เดิม = enrollments) — ไม่แตะตารางที่มีอยู่แล้ว
    Base.metadata.create_all(bind=engine)

    with engine.begin() as conn:
        # 2. คอลัมน์ใหม่ใน courses — create_all ไม่ ALTER ตารางเดิมให้ ต้องเพิ่มเอง
        conn.execute(text("ALTER TABLE courses ADD COLUMN IF NOT EXISTS join_code VARCHAR(8)"))
        conn.execute(text("ALTER TABLE courses ADD COLUMN IF NOT EXISTS join_open BOOLEAN NOT NULL DEFAULT TRUE"))
        conn.execute(text("ALTER TABLE courses ADD COLUMN IF NOT EXISTS section VARCHAR(50)"))
        conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS ix_courses_join_code ON courses (join_code)"))

        # 3. backfill: ทุกคู่ (student, course) ที่มีคะแนนอยู่แล้ว = เคยถูกเพิ่มผ่าน CSV
        # Legacy databases still have scores.section; newer databases do not.
        has_score_section = any(
            column["name"] == "section" for column in inspect(conn).get_columns("scores")
        )
        section_value = "s.section" if has_score_section else "NULL"
        result = conn.execute(text(f"""
            INSERT INTO enrollments (student_id, course_code, section, status, joined_via)
            SELECT DISTINCT ON (s.student_id, q.course_code)
                   s.student_id, q.course_code, {section_value}, 'active', 'csv'
            FROM scores s
            JOIN quizzes q ON q.quiz_id = s.quiz_id
            WHERE s.student_id IS NOT NULL AND q.course_code IS NOT NULL
            ORDER BY s.student_id, q.course_code, s.updated_at DESC NULLS LAST, s.score_id DESC
            ON CONFLICT (student_id, course_code) DO NOTHING
        """))
        print(f"Backfilled enrollments: {result.rowcount}")

    # 4. สร้าง join_code ให้ทุก course ที่ยังไม่มี
    db = SessionLocal()
    try:
        courses = db.query(Course).filter(Course.join_code.is_(None)).all()
        for c in courses:
            c.join_code = generate_join_code(db)
            db.flush()
        db.commit()
        print(f"Generated join codes: {len(courses)}")

        # 5. แถวที่ถูกเชิญผ่าน CSV แต่ยังไม่ได้สมัคร (ยังสมัครได้ผ่าน legacy claim ใน /register)
        pending = db.execute(text("""
            SELECT COUNT(*) FROM auth_users a JOIN students s ON s.auth_user_id = a.auth_user_id
            WHERE a.password IS NULL
        """)).scalar()
        print(f"Legacy invited students not signed up yet: {pending}")
    finally:
        db.close()


if __name__ == "__main__":
    migrate_enrollment()
