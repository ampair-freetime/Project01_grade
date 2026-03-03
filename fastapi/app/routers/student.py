from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Student, Course, Quiz, Score
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

    # ดึงคะแนนทั้งหมดของนักเรียน
    scores = db.query(Score).filter(
        Score.student_id == student.student_id
    ).all()

    # กัน course ซ้ำ
    course_set = set()

    # relationship : Score -> Quiz -> Course
    for s in scores :
        if s.quiz and s.quiz.course:
            course_set.add(s.quiz.course)

    return {
        "student_name": f"{student.first_name} {student.last_name}",
        "student_id": student.student_id,
        "courses": [
            {
                "course_id": c.course_id,
                "course_name": c.course_name
            }
            for c in course_set
        ]
    }


# รายละเอียด course + คะแนนรวม
@router.get("/course/{course_id}")
async def student_course_detail(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):

    # เช็คว่าเป็นนักเรียนจริงไหม
    student = require_student(db, current_user)

    # เช็คว่า course มีอยู่จริงไหม
    course = db.query(Course).filter(
        Course.course_id == course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # ตรวจสอบว่านักเรียนมีคะแนนใน course นี้ไหม
    has_access = db.query(Score).join(Quiz).filter(
        Quiz.course_id == course_id,
        Score.student_id == student.student_id
        ).first()
        
    if not has_access:
        raise HTTPException(
            status_code=403,
            detail="Not enrolled in this course"
        )

    # ดึง quiz ทั้งหมดใน course 
    quizzes = db.query(Quiz).filter(
        Quiz.course_id == course_id
    ).all()

    assessment = []
    total_weight_score = 0
    total_weight = 0

    # ดึงคะแนนทั้งหมด
    student_scores = db.query(Score).join(Quiz).filter(
        Quiz.course_id == course_id,
        Score.student_id == student.student_id
        ).all()
        
    score_map = {s.quiz_id: s for s in student_scores}
    
    for q in quizzes:
        my_score = score_map.get(q.quiz_id)
        score_value = my_score.score if my_score else None
        
        if score_value is not None:
            percent = score_value / q.full_mark
            total_weight_score += percent * q.weight
            total_weight += q.weight

        assessment.append({
            "quiz_id": q.quiz_id,
            "quiz_name": q.quiz_name,
            "weight": q.weight,
            "full_mark": q.full_mark,
            "my_score": score_value,
            "unread_flag": my_score.unread_flag if my_score else False
            })

    # คำนวณ weighted average
    weighted_average = 0
    if total_weight > 0:
        weighted_average = total_weight_score

    return {
        "course_id": course.course_id,
        "course_name": course.course_name,
        "weighted_average": round(weighted_average, 2),
        "assessments": assessment
    }


# ดูคะแนน + สถิติ 
@router.get("/score/{quiz_id}")
async def student_score_detail(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):

    # เช็คว่าเป็นนักเรียนจริงไหม
    student = require_student(db, current_user)

    # ดึงคะแนนของตัวเอง
    my_score = db.query(Score).filter(
        Score.quiz_id == quiz_id,
        Score.student_id == student.student_id
    ).first()

    # ไม่มีคะแนน
    if not my_score:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Score not found"
        )
    
    # mark read
    if my_score.unread_flag:
        my_score.unread_flag = False
        db.commit()

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