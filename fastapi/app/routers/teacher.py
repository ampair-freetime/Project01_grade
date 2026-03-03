from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Teacher, Course, Quiz, Score, Student, Upload, AuthUser
from app.models.authuser import AuthUser
from app.routers.auth import get_current_user
from datetime import datetime
import csv
import io

router = APIRouter()

def is_teacher(db: Session, current_user: AuthUser):
    teacher = db.query(Teacher).filter(Teacher.auth_user_id == current_user.auth_user_id).first()

    if not teacher:
        raise HTTPException(status_code=403, detail="Teacher access only")

    return teacher


# Dashboard 
@router.get("/dashboard_teacher")
async def teacher_dashboard(db: Session = Depends(get_db),current_user: AuthUser = Depends(get_current_user)):
    # ครู?
    teacher = is_teacher(db, current_user)
    # วิชาทั้งหมดที่ครูคนนั้นสร้างไว้
    courses = db.query(Course).filter(Course.teacher_id == teacher.teacher_id).all()
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
async def create_course(course_name: str,db: Session = Depends(get_db),current_user: AuthUser = Depends(get_current_user)):
    # ครู?
    teacher = is_teacher(db, current_user)
    
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


#  upload CSV แสดงว่าต้องมีหน้า quiz name อะไรอย่างนี้แล้ว
@router.post("/upload/{quiz_id}")
async def upload_csv(quiz_id: int,file: UploadFile = File(...),db: Session = Depends(get_db),current_user: AuthUser = Depends(get_current_user)):

    teacher = is_teacher(db, current_user)
    # อ่านละแปลงเป็นข้อความ
    content = await file.read()
    decoded = content.decode("utf-8")
    # แปลงเป็นตาราง
    csv_reader = csv.DictReader(io.StringIO(decoded))

    for row in csv_reader:
        # ดึงข้อมูลจาก CSV
        stu_email = str(row["stu_email"])
        stu_id = int(row["student_id"])
        score_v = float(row["score"])
        section = str(row["section"])

        # เช็ค student มีจริงไหม ถ้าไม่มีใฟ้สร้างใหม่เลย
        user = db.query(AuthUser).filter(AuthUser.email == stu_email).first()

        if not user:
            user = AuthUser(email=stu_email)
            db.add(user)
            db.commit()
            db.refresh(user)
        student = db.query(Student).filter(Student.student_id == stu_id).first()
        if not student:
            new_stu = Student(
                student_id=stu_id,
                auth_user_id=user.auth_user_id)
            db.add(new_stu)
            db.commit()
            db.refresh(new_stu)

        # สร้างหรือ update score ใน quiz นั้นๆ
        # มีคะแนนของ นักเรียน id นี้หรือยัง
        score = db.query(Score).filter(Score.student_id == stu_id,Score.quiz_id == quiz_id).first()
        # ถ้ายังให้สร้าง ถ้ามีให้ update
        if score:
            #update
            score.score = score_v
            score.unread_flag = True
            score.section = section
            db.commit()
        else:
            new_score = Score(
                score = score_v,
                section = section,
                quiz_id = quiz_id,
                student_id = stu_id
            )
            db.add(new_score)
            db.commit()

    return {"message": "CSV uploaded successfully"}

@router.delete("/delete_course")
async def delete_courses():
    # ลบ courses แบบ soft deleted
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
