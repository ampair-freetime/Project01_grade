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
    courses = db.query(Course).filter(Course.teacher_id == teacher.teacher_id,Course.is_deleted == False,Course.is_archive == False).all()
    courses_dash = []
    
    for c in courses:
        student_score = 0
        students = {score.student_id for quiz in c.quizzes for score in quiz.scores}
        if students:
            student_score = len(students)

        get_section = db.query(Score).join(Quiz, Quiz.quiz_id == Score.quiz_id).filter(Quiz.course_code == c.course_code).first()
        if get_section:
            section = get_section.section
        else:
            section= None
        courses_dash.append({
            "course_code": c.course_code,
            "course_name": c.course_name,
            "course_id": c.course_id,
            "number_student": student_score,
            "section":section
        })
    # response ชื่อครูกับรายวิชาที่สอน
    # if not courses:
    #     raise HTTPException(status_code=404,detail="courses not found")
    return {
        "teacher_name": f"{teacher.first_name} {teacher.last_name}",
        "courses": courses_dash
    }

@router.get("/assignment/{course_code}")
async def teacher_assingment(course_code: int,current_user: AuthUser = Depends(get_current_user), db: Session= Depends(get_db)):
    # teacher check
    teacher = is_teacher(db, current_user)
    #ดึง course
    # #check ว่าถ้า เจอ course แล้ว ใช่ของ teacher นี้ไหม
    course = db.query(Course).filter(Course.course_code == course_code,Course.teacher_id == teacher.teacher_id).first()
    if not course:
        raise HTTPException(status_code=404,detail="assignment not found")

    assignment = []
    all_assignment = db.query(Quiz).filter(Quiz.course_code==course_code,Quiz.is_deleted== False).all()
    for q in all_assignment:
        #check is deleted???
        assignment.append({
            "assign_id": q.quiz_id,
            "assign_name": q.quiz_name,
            "full_mark": q.full_mark
        })
    return {
        "course":{
            "course_code": course.course_code,
            "course_name": course.course_name
        },
        "assignment":assignment
    }

@router.get("/stu_score/{quiz_id}")
async def teacher_score(quiz_id: str,db:Session=Depends(get_db),current_user: AuthUser = Depends(get_current_user)):
    teacher = is_teacher(db,current_user)
    #กรองเอา data score ที่เราเคยนำเข้าไว้มาก
    assignment = db.query(Quiz).join(Course).filter(Quiz.quiz_id == quiz_id,Course.teacher_id == teacher.teacher_id).first()
    if not assignment:
        raise HTTPException(status_code=404,detail="score not found")

    student_score = []
    all_score = db.query(Score).filter(Score.quiz_id == quiz_id, Score.is_deleted == False).all()
    for s in all_score:
        # ข้อมูลนักศึกษาสำหรับแสดงชื่อ/รูปโปรไฟล์ในหน้า Grade
        stu = s.student
        student_score.append({
                "score_id": s.score_id,
                "score": s.score,
                "unread_flag": s.unread_flag,
                "section": s.section,
                "stu_id": s.student_id,
                "stu_fname": stu.first_name if stu else None,
                "stu_mname": stu.middle_name if stu else None,
                "stu_lname": stu.last_name if stu else None,
                "avatar_url": stu.avatar_url if stu else None
            })
    return {
        "assignment":{
            "assign_id": assignment.quiz_id,
            "assign_name": assignment.quiz_name
        },
        "score":student_score
    }
# แสดงผล course ที่จัดเก็บไว้ (archive)
@router.get("/archive_teacher")
async def list_archived_courses(db: Session = Depends(get_db), current_user: AuthUser = Depends(get_current_user)):
    teacher = is_teacher(db, current_user)
    courses = db.query(Course).filter(
        Course.teacher_id == teacher.teacher_id,
        Course.is_deleted == False,
        Course.is_archive == True,
    ).all()
    return {
        "teacher_name": f"{teacher.first_name} {teacher.last_name}",
        "courses": [
            {"course_code": c.course_code, "course_name": c.course_name, "course_id":c.course_id}
            for c in courses
        ],
    }

###################################################################################################################################

############################################################### create ############################################################
# สร้าง course เมื่อ login มาแล้ว
@router.post("/create_course")
async def create_course(course: Teacher_Course,db: Session = Depends(get_db),current_user: AuthUser = Depends(get_current_user)):
    # ครู?
    try:
        teacher = is_teacher(db, current_user)

        new_course = Course(
            course_name=course.course_name,
            teacher_id=teacher.teacher_id,
            course_id=course.course_id
        )

        db.add(new_course)
        db.commit()
        db.refresh(new_course)

        return {
            "message": "Course created successfully",
            "course_code": new_course.course_code
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,detail=f"error: {str(e)}") 

@router.post("/create_assign")
async def create_assignments(assign: T_Assignment,db: Session= Depends(get_db),current_user: AuthUser = Depends(get_current_user)):
    try:
        teacher = is_teacher(db,current_user)
        # if ()
        new_assignment = Quiz(
            quiz_name=assign.quiz_name,
            full_mark=assign.full_mark,
            course_code=assign.course_code
        )

        db.add(new_assignment)
        db.commit()
        db.refresh(new_assignment)
        #สร้าง assignment
        return {
            "message":"Assignment created succeddfully",
            "assign_id": new_assignment.quiz_id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,detail=f"error: {str(e)}") 


####################################################################################################################################
#  upload CSV แสดงว่าต้องมีหน้า quiz name อะไรอย่างนี้แล้ว
@router.post("/upload/{course_code}/{quiz_id}")
async def upload_csv(quiz_id: str,course_code: int,file: UploadFile = File(...),db: Session = Depends(get_db),current_user: AuthUser = Depends(get_current_user)):
    try:
        teacher = is_teacher(db, current_user)
        # ถ้ามีการ upload อีกครั้ง ก็ให้ยัง ไม่publish ต้องกดอีกครั้งถึงจะ publish
        assignment = db.query(Quiz).join(Course).filter(Quiz.quiz_id == quiz_id,Course.teacher_id==teacher.teacher_id).first()
        if assignment.is_publish:
            assignment.is_publish = False
        file_name = file.filename
        new_upload = Upload(
            file_name=file_name,
            teacher_id = teacher.teacher_id,
            course_code=course_code
        )
        db.add(new_upload)
        db.commit()
        db.refresh(new_upload)
        # อ่านละแปลงเป็นข้อความ
        content = await file.read()
        decoded = content.decode("utf-8-sig")
        # แปลงเป็นตาราง
        csv_reader = list(csv.DictReader(io.StringIO(decoded), delimiter=','))

        emails_stu = [row["student_email"] for row in csv_reader]
        id_stu = [row["student_id"] for row in csv_reader]
        #หา user student ที่มี email ในนี้แล้ว แสดงว่าเราแค่เพิ่มหรือแก้ไขคะแนน
        stu_signup = db.query(Student).join(AuthUser).filter(Student.student_id.in_(id_stu),AuthUser.email.in_(emails_stu)).all()
        stu_index = {}
        for u in stu_signup:
            stu_index[u.student_id] = u
        all_score =  db.query(Score).filter(Score.student_id.in_(id_stu),Score.quiz_id==quiz_id).all()
        score_index = {}
        for s in all_score:
            score_index[s.student_id] = s
        #ให้สร้างไอดี ใหม่ก่อนถ้ายังไมมี
        for row in csv_reader:
            stu_email = str(row["student_email"])
            stu_id = str(row["student_id"])
            score_v = float(row["score"])
            section = str(row["section"])
            name = str(row["name"]).strip()
            name = name.split()

            middle_name = None
            last_name = None
            if len(name) > 2:
                middle_name = name[1]
                last_name = name[2]
            else:
                last_name = name[1]
            #ไม่มี ไอดีให้สร้างใหม่
            t_stu = stu_index.get(stu_id)
            if not t_stu:
                new_user = AuthUser(email=stu_email)
                db.add(new_user)
                db.flush()

                new_stu = Student(
                    student_id=stu_id,
                    auth_user_id=new_user.auth_user_id,
                    first_name=name[0],
                    middle_name=middle_name,
                    last_name=last_name
                    )
                db.add(new_stu)
                stu_index[stu_id] = new_stu
            else:
                pass
            t_score = score_index.get(stu_id)

            if t_score:
                # Update คะแนนเดิม
                t_score.score = score_v
                t_score.section = section
                t_score.unread_flag = True
                t_score.is_deleted = False
            else:
                # สร้างคะแนนใหม่
                new_score = Score(
                        score=score_v,
                        section=section,
                        quiz_id=quiz_id,
                        student_id=stu_id
                    ) #
                db.add(new_score)
        db.commit()


        return {"message": "CSV uploaded successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,detail=f"Upload failed: {str(e)}")
############################################################################ deleted #####################################################################
@router.post("/delete_course/{course_code}")
async def delete_courses(course_code:int,db: Session = Depends(get_db),current_user: AuthUser = Depends(get_current_user)):
    # ลบ courses แบบ soft deleted'
    try:
        teacher = is_teacher(db,current_user)
        course = db.query(Course).filter(Course.course_code == course_code,Course.teacher_id == teacher.teacher_id).first()
        if not course:
            raise HTTPException(status=404,detail="course not found")
        course.is_deleted = True
        db.commit()
        return {"message":"deleted course successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,detail=f"error: {str(e)}") 

@router.post("/delete_assign/{assign_id}")
async def delete_assignments(assign_id:str,db: Session = Depends(get_db),current_user: AuthUser = Depends(get_current_user)):
    #ลบ assignment
    try:
        teacher = is_teacher(db,current_user)
        assignment = db.query(Quiz).join(Course).filter(Quiz.quiz_id == assign_id,Course.teacher_id == teacher.teacher_id).first()
        if not assignment:
            raise HTTPException(status=404,detail="assignment not found")
        assignment.is_deleted = True
        db.commit()
        return {"message":"deleted assignment successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,detail=f"error: {str(e)}") 

@router.post("/delete_score/{assign_id}/{score_id}")
async def delete_assignments(score_id:str,assign_id:str,db: Session = Depends(get_db),current_user: AuthUser = Depends(get_current_user)):
    #ลบ assignment
    try:
        teacher = is_teacher(db,current_user)
        #หา Quiz ที่เชื่อมกับอาจารคนนี้ก่อน และส่งมาเป็น quiz ไหน
        assignment = db.query(Quiz).join(Course).filter(Quiz.quiz_id == assign_id,Course.teacher_id == teacher.teacher_id).first()
        # เอา quiz ที่หามาได้ไปหา score ใน database อีกที
        score = db.query(Score).filter(Score.score_id == score_id,Score.quiz_id == assignment.quiz_id).first()
        if not score:
            raise HTTPException(status=404,detail="Score not found")
        score.is_deleted = True
        db.commit()
        return {"message":"deleted score successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,detail=f"error: {str(e)}") 
###########################################################################################################################################################

@router.post("/archive/{course_code}")
async def archive(course_code:int, db:Session = Depends(get_db), current_user: AuthUser=Depends(get_current_user)):
    try:
        teacher = is_teacher(db,current_user)
        course = db.query(Course).filter(Course.course_code == course_code,Course.teacher_id == teacher.teacher_id).first()
        #จัดเก็บ course
        if not course:
            raise HTTPException(status=404,detail="Course not found")
        course.is_archive = True
        db.commit()
        return {"message":"Archive course successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,detail=f"error: {str(e)}") 

@router.post("/restore_to_dash/{course_code}")
async def restore_course(course_code: int, db: Session = Depends(get_db), current_user: AuthUser = Depends(get_current_user)):
    try:
        teacher = is_teacher(db, current_user)
        course = db.query(Course).filter(Course.course_code == course_code,Course.teacher_id == teacher.teacher_id,).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        course.is_archive = False
        db.commit()
        return {"message": "Restore course successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,detail=f"error: {str(e)}") 

@router.post("/publish/{assign_id}")
async def publish(assign_id:str,db: Session = Depends(get_db),current_user: AuthUser = Depends(get_current_user)):
    try:
        teacher = is_teacher(db,current_user)
        assignment = db.query(Quiz).join(Course).filter(Quiz.quiz_id == assign_id,Course.teacher_id==teacher.teacher_id).first()
        if not assignment:
            raise HTTPException(status_code=404,detail="Assignment not found")
        if assignment.is_publish:
            raise HTTPException(status_code=409,detail="This assignment is already published")
        assignment.is_publish = True
        db.commit()

        return {"message": "Publish successful"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,detail=f"error: {str(e)}") 
