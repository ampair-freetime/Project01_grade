# fastapi/app/seed.py
from app.db import SessionLocal, engine, Base
from app.models import AuthUser, UserRole, Course, Enrollment

def seed_data():
    db = SessionLocal()

    # 2. เช็คว่ามีข้อมูลหรือยัง ถ้ามีแล้วไม่สร้างซ้ำ
    if db.query(AuthUser).first():
        print("Database already contains data. Skipping seed.")
        return

    print("🌱 Seeding data...")

    # --- สร้าง Teacher ---
    teacher = AuthUser(
        email="teacher@cmu.ac.th",
        name="Dr. Somchai (Teacher)",
        avatar_url="https://ui-avatars.com/api/?name=Teacher",
        role=UserRole.TEACHER,
        # password=... (ถ้ามีฟิลด์ password)
    )
    db.add(teacher)
    db.commit() # Commit เพื่อให้ได้ ID

    # --- สร้าง Student ---
    student = AuthUser(
        email="student@cmu.ac.th",
        name="Nong Som (Student)",
        avatar_url="https://ui-avatars.com/api/?name=Student",
        role=UserRole.STUDENT,
        student_id="650510001" # รหัสนักศึกษา
    )
    db.add(student)
    db.commit()

    # --- สร้าง Course (วิชา) ---
    course_cs101 = Course(
        code="CS101",
        name="Intro to Computer Science",
        teacher_id=teacher.id
    )
    db.add(course_cs101)
    db.commit()

    # --- สร้าง Enrollment (ลงทะเบียนเรียน + เกรด) ---
    grade = Enrollment(
        student_id=student.id,
        course_id=course_cs101.id,
        score=85.5
    )
    db.add(grade)
    db.commit()

    print(" Seeding complete!")
    print(f"Teacher: {teacher.email}")
    print(f"Student: {student.email} (ID: {student.student_id})")
    print(f"Course: {course_cs101.code}")
    
    db.close()

if __name__ == "__main__":
    seed_data()