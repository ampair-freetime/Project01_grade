# fastapi/app/manage.py
from app.db import SessionLocal
# 🌟 แก้ไขบรรทัดนี้: ลบ Enrollment ออก เอา Quiz กับ Score เข้ามาแทน
from app.models import AuthUser, Teacher, Student, Course, Quiz, Score 
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def seed_data():
    db = SessionLocal()

    if db.query(AuthUser).first():
        print("Database already contains data. Skipping seed.")
        return

    hashed_password = password_hash.hash("123456")

    teacher_auth = AuthUser(email="som.jai@cmu.ac.th", password=hashed_password)
    db.add(teacher_auth)
    db.commit()
    db.refresh(teacher_auth)

    teacher_profile = Teacher(first_name="Somchai", last_name="Jaidee", auth_user_id=teacher_auth.auth_user_id)
    db.add(teacher_profile)
    db.commit()
    db.refresh(teacher_profile)

    student_auth = AuthUser(email="som_r@cmu.ac.th", password=hashed_password)
    db.add(student_auth)
    db.commit()
    db.refresh(student_auth)

    student_profile = Student(student_id="650510001", first_name="Nong Som", last_name="Roy", auth_user_id=student_auth.auth_user_id)
    db.add(student_profile)
    db.commit()
    db.refresh(student_profile)

    student_auth2 = AuthUser(email="nudee_k@cmu.ac.th", password=hashed_password)
    db.add(student_auth2)
    db.commit()
    db.refresh(student_auth2)

    student_profile2 = Student(student_id="650510555", first_name="Nu dee", last_name="kimnum", auth_user_id=student_auth2.auth_user_id)
    db.add(student_profile2)
    db.commit()
    db.refresh(student_profile2)

    course_cs101 = Course(course_name="Intro to Computer Science", teacher_id=teacher_profile.teacher_id)
    db.add(course_cs101)
    db.commit()
    db.refresh(course_cs101)

    assignment_1 = Quiz(
        quiz_name="Assignment 1",
        full_mark=30,
        course_code=course_cs101.course_code
    )
    db.add(assignment_1)
    db.commit()
    db.refresh(assignment_1)

    student_score = Score(
        score=24.0, 
        unread_flag=True, 
        section="001", 
        student_id=student_profile.student_id, 
        quiz_id=assignment_1.quiz_id
    )
    db.add(student_score)
    db.commit()

    student_score2 = Score(
        score=28.0,
        unread_flag=True, 
        section="001", 
        student_id=student_profile2.student_id, 
        quiz_id=assignment_1.quiz_id
    )
    db.add(student_score2)
    db.commit()
    print("Seeding Complete!")
    db.close()

if __name__ == "__main__":
    seed_data()