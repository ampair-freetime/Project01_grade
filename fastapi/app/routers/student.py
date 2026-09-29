from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Student, Course, Quiz, Score, Enrollment
from app.models.authuser import AuthUser
from app.routers.auth import get_current_user
from app.schemas.student import EnrollRequest
from collections import defaultdict, deque
import time

router = APIRouter()

# กันเดา join code: กรอกผิดได้ไม่เกิน 10 ครั้ง / 10 นาที ต่อนักศึกษา
# (เก็บใน memory ของแต่ละ worker — พอสำหรับกันเดาแบบง่ายๆ)
JOIN_FAIL_LIMIT = 10
JOIN_FAIL_WINDOW = 600
join_failures = defaultdict(deque)

# ตรวจสอบว่าเป็นนักเรียนจริงไหม
def require_student(db: Session, current_user: AuthUser):

    student = db.query(Student).filter(Student.auth_user_id == current_user.auth_user_id).first()

    if not student:
        raise HTTPException(status_code=403,detail="You are not registered as a student")

    return student


def teacher_full_name(teacher):
    if teacher.middle_name:
        return teacher.first_name + " " + teacher.middle_name + " " + teacher.last_name
    return teacher.first_name + " " + teacher.last_name


def active_enrollment(db: Session, student_id: str, course_code: int):
    return db.query(Enrollment).filter(
        Enrollment.student_id == student_id,
        Enrollment.course_code == course_code,
        Enrollment.status == "active",
    ).first()


def check_join_rate(student_id: str):
    now = time.time()
    fails = join_failures[student_id]
    while fails and now - fails[0] > JOIN_FAIL_WINDOW:
        fails.popleft()
    if len(fails) >= JOIN_FAIL_LIMIT:
        raise HTTPException(status_code=429, detail="Too many attempts. Please try again later.")


# หา course จาก join code + เช็คว่า join ได้ไหม (ใช้ทั้งตอน preview และตอน enroll)
def find_joinable_course(db: Session, student: Student, code: str):
    check_join_rate(student.student_id)
    code = code.strip().upper()
    course = db.query(Course).filter(Course.join_code == code, Course.is_deleted == False, Course.is_archive == False).first() if code else None
    if not course:
        join_failures[student.student_id].append(time.time())
        raise HTTPException(status_code=404, detail="Invalid join code. Please check the code and try again.")
    if active_enrollment(db, student.student_id, course.course_code):
        raise HTTPException(status_code=409, detail="You are already enrolled in this course.")
    if not course.join_open:
        raise HTTPException(status_code=403, detail="Enrollment is closed. Please contact your teacher.")
    return course


def course_summary(course: Course):
    return {
        "course_code": course.course_code,
        "course_name": course.course_name,
        "course_id": course.course_id,
        "teacher_name": teacher_full_name(course.teacher),
    }


# ดูข้อมูลวิชาก่อนกดยืนยัน join
@router.get("/enroll/{code}")
async def preview_enroll(code: str, db: Session = Depends(get_db), current_user: AuthUser = Depends(get_current_user)):
    student = require_student(db, current_user)
    return course_summary(find_joinable_course(db, student, code))


# join วิชาด้วย join code
@router.post("/enroll")
async def enroll(body: EnrollRequest, db: Session = Depends(get_db), current_user: AuthUser = Depends(get_current_user)):
    student = require_student(db, current_user)
    course = find_joinable_course(db, student, body.code)
    try:
        enrollment = db.query(Enrollment).filter(Enrollment.student_id == student.student_id, Enrollment.course_code == course.course_code).first()
        if enrollment:
            # เคยถูกเอาออก (dropped) แล้ว join กลับมาใหม่
            enrollment.status = "active"
        else:
            db.add(Enrollment(student_id=student.student_id, course_code=course.course_code, status="active", joined_via="code"))
        db.commit()
    except IntegrityError:
        # กด join พร้อมกัน 2 ครั้ง
        db.rollback()
        raise HTTPException(status_code=409, detail="You are already enrolled in this course.")
    return {"message": "Enrolled successfully", "course": course_summary(course)}


# Dashboard 
@router.get("/dashboard_student")
async def student_dashboard(db: Session = Depends(get_db),current_user: AuthUser = Depends(get_current_user)):
    # เช็คว่าเป็นนักเรียนจริงไหม
    student = require_student(db, current_user)

    # วิชาที่ join อยู่ (enrollments) — วิชาที่เพิ่ง join แต่ยังไม่มีคะแนนก็โชว์
    enrollments = db.query(Enrollment).join(Course).filter(
        Enrollment.student_id == student.student_id,
        Enrollment.status == "active",
        Course.is_deleted == False,
    ).order_by(Enrollment.created_at.desc()).all()

    course_dash = []
    for e in enrollments:
        course_dash.append({
            "course_code": e.course.course_code,
            "course_name": e.course.course_name,
            "course_id": e.course.course_id,
            "section": e.section,
            "teacher_name": teacher_full_name(e.course.teacher),
        })

    return {
        "student_name": f"{student.first_name} {student.last_name}",
        "student_id": student.student_id,
        "courses": course_dash
    }


# รายละเอียด course + คะแนนรวม
@router.get("/course/{course_code}")
async def student_course_detail(course_code: int,db: Session = Depends(get_db),current_user: AuthUser = Depends(get_current_user)):

    # เช็คว่าเป็นนักเรียนจริงไหม
    student = require_student(db, current_user)

    # เช็คว่า course มีอยู่จริงไหม
    course = db.query(Course).filter(Course.course_code == course_code, Course.is_deleted == False).first()

    if not course:
        raise HTTPException(status_code=404,detail="Course not found")
    
    # ตรวจสอบว่านักเรียนอยู่ใน course นี้ไหม (ยังไม่มีคะแนนก็เข้าได้ แค่ assessments ว่าง)
    enrollment = active_enrollment(db, student.student_id, course_code)

    if not enrollment:
        raise HTTPException(status_code=403,detail="Not enrolled in this course")

    # ดึง quiz ทั้งหมดใน course 
    quizzes = db.query(Quiz).filter(Quiz.course_code == course_code,Quiz.is_deleted==False,Quiz.is_publish==True).all()

    # ดึงคะแนนทั้งหมด
    student_scores = db.query(Score).join(Quiz).filter(
        Quiz.course_code == course_code,
        Score.student_id == student.student_id,
        Score.is_deleted == False,
        Quiz.is_deleted == False
    ).all()

    score_map = {s.quiz_id: s for s in student_scores}

    assessment = []
    total_weight_score = 0
    total_weight = sum(q.weight for q in quizzes)

    for q in quizzes:
        my_score = score_map.get(q.quiz_id)
        score_value = my_score.score if my_score else None

        percent = None

        if score_value is not None and q.full_mark > 0:
            percent = round((score_value / q.full_mark) * 100, 2)
            total_weight_score += (score_value / q.full_mark) * q.weight

        assessment.append({
            "quiz_id": q.quiz_id,
            "quiz_name": q.quiz_name,
            "weight": q.weight,
            "full_mark": q.full_mark,
            "my_score": score_value,
            "percent": percent,
            "unread_flag": my_score.unread_flag if my_score else False
            })

    # คำนวณ weighted average
    weighted_average = 0
    if total_weight > 0:
        weighted_average = round((total_weight_score / total_weight) * 100, 2)
    return {
        "course_code": course.course_code,
        "course_name": course.course_name,
        "course_id": course.course_id,
        "section": enrollment.section,
        "teacher_name": teacher_full_name(course.teacher),
        "weighted_average": weighted_average,
        "assessments": assessment
    }


# ดูคะแนน + สถิติ 
@router.get("/score/{quiz_id}")
async def student_score_detail(quiz_id: str,db: Session = Depends(get_db),current_user: AuthUser = Depends(get_current_user)):

    # เช็คว่าเป็นนักเรียนจริงไหม
    try:
        student = require_student(db, current_user)

        # ดึงคะแนนของตัวเอง
        my_score = db.query(Score).filter(Score.quiz_id == quiz_id,Score.student_id == student.student_id,Score.is_deleted==False).first()

        # ไม่มีคะแนน
        if not my_score:
            raise HTTPException(status_code=404,detail="Score not found")

        # ถูกเอาออกจากวิชาแล้ว ดูคะแนนไม่ได้
        if not active_enrollment(db, student.student_id, my_score.quiz.course_code):
            raise HTTPException(status_code=403,detail="Not enrolled in this course")
        
        # mark read
        if my_score.unread_flag:
            my_score.unread_flag = False
            db.commit()

        # คะแนนของทุกคน 
        all_scores = db.query(Score).filter(Score.quiz_id == quiz_id,Score.is_deleted==False).all()

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
                "lowest": 0,
                "total_students": 0,
                "ranking": None
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
        variance = sum((x - mean) ** 2 for x in score_list) / n
        std = variance ** 0.5

        # คำนวณเปอร์เซ็น
        if my_score.quiz.full_mark > 0:
            percent = round((my_score.score / my_score.quiz.full_mark) * 100, 2)
        else:
            percent = 0

        # ranking
        ranking = sum(1 for s in score_list if s > my_score.score) + 1

        return {
            "my_score": my_score.score,
            "full_mark": my_score.quiz.full_mark,
            "percent": percent,
            "mean": round(mean, 2),
            "median": round(median, 2),
            "std": round(std, 2),
            "highest": highest,
            "lowest": lowest,
            "total_students": len(score_list),
            "ranking": ranking
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,detail=f"error: {str(e)}")