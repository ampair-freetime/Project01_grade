from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Teacher, Course, Quiz, Score, Student
from app.models.authuser import AuthUser
from app.routers.auth import get_current_user
import csv
import io

router = APIRouter()

# ตรวจสอบว่าเป็นอาจารย์จริงไหม
def require_teacher(db: Session, current_user: AuthUser):

    teacher = db.query(Teacher).filter(
        Teacher.auth_user_id == current_user.auth_user_id
    ).first()

    if not teacher:
        raise HTTPException(status_code=403, detail="Teacher access only")

    return teacher


# Dashboard 
@router.get("/dashboard_teacher")
async def teacher_dashboard(
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    # เช็คว่าเป็นอาจารย์จริงไหม
    teacher = require_teacher(db, current_user)
    # วิชาทั้งหมดที่สอน
    courses = db.query(Course).filter(
        Course.teacher_id == teacher.teacher_id
    ).all()
    # response ชื่อครูกับรายวิชาที่สอน
    return {
        "teacher_name": f"{teacher.first_name} {teacher.last_name}",
        "courses": [
            {
                "course_id": c.course_id,
                "course_name": c.course_name
            }
            for c in courses
        ]
    }


# สร้าง course
@router.post("/create_course")
async def create_course(
    # ชื่อวิชา
    course_name: str,
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    # ตรวจว่าเป็นอาจารย์
    teacher = require_teacher(db, current_user)
    # สร้างวิชาใหม่และเป็นชื่ออาจารย์คนเดิม
    new_course = Course(
        course_name=course_name,
        teacher_id=teacher.teacher_id
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return {
        "message": "Course created successfully",
        "course_id": new_course.course_id
    }


#  upload CSV 
@router.post("/upload")
async def upload_csv(
    # รับไฟล์มา
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):

    teacher = require_teacher(db, current_user)

    # อ่านละแปลงเป็นข้อความ
    content = await file.read()
    decoded = content.decode("utf-8")
    # แปลงเป็นตาราง
    csv_reader = csv.DictReader(io.StringIO(decoded))

    for row in csv_reader:
        # ดึงข้อมูลจาก CSV
        student_id = int(row["student_id"])
        quiz_id = int(row["quiz_id"])
        score_value = float(row["score"])

        # เช็ค student มีจริงไหม
        student = db.query(Student).filter(
            Student.student_id == student_id
        ).first()

        if not student:
            continue

        # สร้างหรือ update score
        score = db.query(Score).filter(
            Score.student_id == student_id,
            Score.quiz_id == quiz_id
        ).first()

        if score:
            score.score = score_value
        else:
            new_score = Score(
                student_id=student_id,
                quiz_id=quiz_id,
                score=score_value
            )
            db.add(new_score)

    db.commit()

    return {"message": "CSV uploaded successfully"}

@router.delete("/delete_course")
async def delete_courses():
    # ลบ courses 
    return ...

# ? หรือควรสร้าง post อันเดียว แยก course กับ assign ?
@router.post("/created_assign")
async def create_assignments():
    #สร้าง assignment
    return ...

# ? หรือควรสร้าง delete อันเดียว แยก course กับ assign ?
@router.delete("/delete_assign")
async def delete_assignments():
    #ลบ assignment
    return ...
