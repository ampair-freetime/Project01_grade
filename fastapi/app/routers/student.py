from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db import get_db
from app.models import Student, Enrollment, Course, Quiz, Score, Teacher
from app.models.authuser import AuthUser
from app.routers.auth import get_current_user

router = APIRouter()

# ตรวจสอบว่าเป็นนักเรียนจริงไหม
def require_student(db: Session, current_user: AuthUser):

    student = db.query(Student).filter(
        Student.auth_user_id == current_user.auth_user_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not registered as a student"
        )

    return student


# Dashboard 
@router.get("/dashboard_student")
async def student_dashboard(
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    # เช็คว่าเป็นนักเรียนจริงไหม
    student = require_student(db, current_user)
    # courses ที่ลง
    courses = (
        db.query(Course)
        .join(Enrollment, Enrollment.course_id == Course.course_id)
        .filter(Enrollment.student_id == student.student_id)
        .all()
    )

    return {
        "student_name": f"{student.first_name} {student.last_name}",
        "student_id": student.student_id,
        "courses": [
            {
                "course_id": c.course_id,
                "course_name": c.course_name
            }
            for c in courses
        ]
    }


# รายละเอียด course 
@router.get("/courses/{course_id}")
async def student_course_detail(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):

    student = require_student(db, current_user)

    # เช็คว่าลงทะเบียนวิชานี้ไหม
    enrollment = db.query(Enrollment).filter(
        Enrollment.student_id == student.student_id,
        Enrollment.course_id == course_id
    ).first()
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enrolled in this course"
        )

    # ดึง quiz
    quizzes = db.query(Quiz).filter(
        Quiz.course_id == course_id
    ).all()

    result = []

    for q in quizzes:
        my_score = db.query(Score).filter(
            Score.quiz_id == q.quiz_id,
            Score.student_id == student.student_id
        ).first()

        result.append({
            "quiz_id": q.quiz_id,
            "quiz_name": q.quiz_name,
            "weight": q.weight,
            "my_score": my_score.score if my_score else None
        })

    return {
        "course_id": course_id,
        "assessments": result
    }


# ดูคะแนน + สถิติ 
@router.get("/score/{quiz_id}")
async def student_score_detail(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):

    student = require_student(db, current_user)

    # คะแนนของตัวเอง
    my_score = db.query(Score).filter(
        Score.quiz_id == quiz_id,
        Score.student_id == student.student_id
    ).first()

    if not my_score:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Score not found"
        )

    # คะแนนของทุกคน 
    all_scores = db.query(Score).filter(
        Score.quiz_id == quiz_id
    ).all()

    score_list = [s.score for s in all_scores if s.score is not None]

    if not score_list:
        return {
            "my_score": my_score.score,
            "full_mark": my_score.quiz.full_mark,
            "percent": 0,
            "mean": 0,
            "median": 0,
            "std": 0,
            "highest": 0,
            "lowest": 0
        }

    # คำนวณ mean
    mean = sum(score_list) / len(score_list)
    # คะแนนสูงสุด
    highest = max(score_list)
    # คะแนนต้ำสุด
    lowest = min(score_list)
    # เรียงลำดับ
    sort_score = sorted(score_list)
    n = len(sort_score)

    # คำนวณ median
    if n % 2 == 0:
        median = (sort_score[n//2 - 1] + sort_score[n//2]) / 2
    else:
        median = sort_score[n//2]

    # คำนวณ std
    variance = sum((x - mean) ** 2 for x in score_list) / len(score_list)
    std = variance ** 0.5
    # คำนวณเปอร์เซ็น
    percent = (my_score.score / my_score.quiz.full_mark) * 100

    return {
        "my_score": my_score.score,
        "full_mark": my_score.quiz.full_mark,
        "percent": round(percent, 2),
        "mean": round(mean, 2),
        "median": round(median, 2),
        "std": round(std, 2),
        "highest": highest,
        "lowest": lowest
    }