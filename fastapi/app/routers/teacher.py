from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Teacher, Course, Quiz, Score, Student, Upload, AuthUser
from app.models.authuser import AuthUser
from app.routers.auth import get_current_user
from app.schemas.teacher import Teacher_Course, T_Assignment
from datetime import datetime
import csv
import io

router = APIRouter()

def is_teacher(db: Session, current_user: AuthUser):
    teacher = db.query(Teacher).filter(Teacher.auth_user_id == current_user.auth_user_id).first()

    if not teacher:
        raise HTTPException(status_code=403, detail="Teacher access only")

    return teacher

########################################################## แสดงผลต่างๆ ############################################
# Dashboard 
@router.get("/dashboard_teacher")
async def teacher_dashboard(db: Session = Depends(get_db),current_user: AuthUser = Depends(get_current_user)):
    # ครู?
    teacher = is_teacher(db, current_user)
    # วิชาทั้งหมดที่ครูคนนั้นสร้างไว้
    courses = db.query(Course).filter(Course.teacher_id == teacher.teacher_id,Course.is_deleted == False).all()
    # response ชื่อครูกับรายวิชาที่สอน
    if not courses:
        raise HTTPException(status_code=404,detail="courses not found")
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

@router.get("/assignment/{course_id}")
async def teacher_assingment(course_id: int,current_user: AuthUser = Depends(get_current_user), db: Session= Depends(get_db)):
    # teacher check
    teacher = is_teacher(db, current_user)
    #ดึง course
    # #check ว่าถ้า เจอ course แล้ว ใช่ของ teacher นี้ไหม
    course = db.query(Course).filter(Course.course_id == course_id,Course.teacher_id == teacher.teacher_id).first()
    if not course:
        raise HTTPException(status_code=404,detail="assignment not found")

    assignment = []
    
    for q in course.quizzes:
        #check is deleted???
        if q.is_deleted == False:
            assignment.append({
                "assign_id": q.quiz_id,
                "assign_name": q.quiz_name,
                "full_mark": q.full_mark
            })
    return {
        "course":{
            "course_id": course.course_id,
            "course_name": course.course_name
        },
        "assignment":assignment
    }

@router.get("/stu_score/{quiz_id}")
async def teacher_score(quiz_id: int,db:Session=Depends(get_db),current_user: AuthUser = Depends(get_current_user)):
    teacher = is_teacher(db,current_user)
    #กรองเอา data score ที่เราเคยนำเข้าไว้มาก
    assignment = db.query(Quiz).join(Course).filter(Quiz.quiz_id == quiz_id,Course.teacher_id == teacher.teacher_id).first()
    if not assignment:
        raise HTTPException(status_code=404,detail="score not found")

    student_score = []
    
    for s in assignment.scores:
        #check is deleted???
        if s.is_deleted == False:
            student_score.append({
                "score_id": s.score_id,
                "score": s.score,
                "unread_flag": s.unread_flag,
                "section": s.section,
                "stu_id":s.student_id
            })
    return {
        "assignment":{
            "assign_id": assignment.quiz_id,
            "assign_name": assignment.quiz_name
        },
        "score":student_score
    }
#แสดงผล course ที่จัดเก็บไว้
@router.get("/archive_teacher")
async def teacher_dashboard(db: Session = Depends(get_db),current_user: AuthUser = Depends(get_current_user)):
    # ครู?
    teacher = is_teacher(db, current_user)
    # วิชาทั้งหมดที่ครูคนนั้นสร้างไว้
    courses = db.query(Course).filter(Course.teacher_id == teacher.teacher_id,Course.is_deleted == False,Course.is_archive == True).all()
    # response ชื่อครูกับรายวิชาที่สอน
    if not courses:
        raise HTTPException(status_code=404,detail="courses not found")
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

###################################################################################################################################

############################################################### create ############################################################
# สร้าง course เมื่อ login มาแล้ว
@router.post("/create_course")
async def create_course(course: Teacher_Course,db: Session = Depends(get_db),current_user: AuthUser = Depends(get_current_user)):
    # ครู?
    teacher = is_teacher(db, current_user)
    
    new_course = Course(
        course_name=course.course_name,
        teacher_id=teacher.teacher_id
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return {
        "message": "Course created successfully",
        "course_id": new_course.course_id
    }

@router.post("/create_assign")
async def create_assignments(assign: T_Assignment,db: Session= Depends(get_db),current_user: AuthUser = Depends(get_current_user)):
    teacher = is_teacher(db,current_user)

    new_assignment = Quiz(
        quiz_name=assign.quiz_name,
        full_mark=assign.full_mark,
        course_id=assign.course_id
    )

    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    #สร้าง assignment
    return {
        "message":"Assignment created succeddfully",
        "assign_id": new_assignment.quiz_id
    }


####################################################################################################################################
#  upload CSV แสดงว่าต้องมีหน้า quiz name อะไรอย่างนี้แล้ว
@router.post("/upload/{quiz_id}")
async def upload_csv(quiz_id: int,file: UploadFile = File(...),db: Session = Depends(get_db),current_user: AuthUser = Depends(get_current_user)):

    teacher = is_teacher(db, current_user)
    # อ่านละแปลงเป็นข้อความ
    content = await file.read()
    decoded = content.decode("utf-8-sig")
    # แปลงเป็นตาราง
    csv_reader = csv.DictReader(io.StringIO(decoded))
    # if csv_reader:
    #     raise HTTPException(status=404,detail=f"Header: {csv_reader.fieldnames}")

    for row in csv_reader:
        # ดึงข้อมูลจาก CSV
        stu_email = str(row["student_email"])
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
############################################################################ deleted #####################################################################
@router.post("/delete_course/{course_id}")
async def delete_courses(course_id:int,db: Session = Depends(get_db),current_user: AuthUser = Depends(get_current_user)):
    # ลบ courses แบบ soft deleted'
    teacher = is_teacher(db,current_user)
    course = db.query(Course).filter(Course.course_id == course_id,Course.teacher_id == teacher.teacher_id)
    if not course:
        raise HTTPException(status=404,detail="course not found")
    course.is_deleted = True
    db.commit()
    return {"message":"deleted course successfully"}


# ? หรือควรสร้าง delete อันเดียว แยก course กับ assign ?
@router.post("/delete_assign/{assign_id}")
async def delete_assignments(assign_id:int,db: Session = Depends(get_db),current_user: AuthUser = Depends(get_current_user)):
    #ลบ assignment
    teacher = is_teacher(db,current_user)
    assignment = db.query(Quiz).join(Course).filter(Quiz.quiz_id == assign_id,Course.teacher_id == teacher.teacher_id)
    if not assignment:
        raise HTTPException(status=404,detail="assignment not found")
    assignment.is_deleted = True
    db.commit()
    return {"message":"deleted assignment successfully"}

@router.post("/delete_score/{assign_id}/{score_id}")
async def delete_assignments(score_id:int,assign_id:int,db: Session = Depends(get_db),current_user: AuthUser = Depends(get_current_user)):
    #ลบ assignment
    teacher = is_teacher(db,current_user)
    #หา Quiz ที่เชื่อมกับอาจารคนนี้ก่อน และส่งมาเป็น quiz ไหน
    assignment = db.query(Quiz).join(Course).filter(Quiz.quiz_id == assign_id,Course.teacher_id == teacher.teacher_id)
    # เอา quiz ที่หามาได้ไปหา score ใน database อีกที
    score = db.query(Score).filter(Score.score_id == score_id,Score.quiz_id == assignment.quiz_id)
    if not score:
        raise HTTPException(status=404,detail="Score not found")
    score.is_deleted = True
    db.commit()
    return {"message":"deleted score successfully"}
###########################################################################################################################################################

@router.post("/archive/{course_id}")
async def archive(course_id:int, db:Session = Depends(get_db), current_user: AuthUser=Depends(get_current_user)):
    teacher = is_teacher(db,current_user)
    course = db.query(Course).filter(Course.course_id == course_id,Course.teacher_id == teacher.teacher_id)
    #จัดเก็บ course
    if not course:
        raise HTTPException(status=404,detail="Course not found")
    course.is_archive = True
    return {"message":"Archive course successfully"}