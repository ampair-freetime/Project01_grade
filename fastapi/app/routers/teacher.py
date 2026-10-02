from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Teacher, Course, Quiz, Score, Student, Upload, AuthUser, Enrollment
from app.models.authuser import AuthUser
from app.routers.auth import get_current_user
from app.schemas.teacher import Teacher_Course, Assignment, CourseUpdate,AssignmentUpdate
from app.join_code import generate_join_code
from datetime import datetime
import csv
import io

router = APIRouter()

def is_teacher(db: Session, current_user: AuthUser):
    teacher = db.query(Teacher).filter(Teacher.auth_user_id == current_user.auth_user_id).first()

    if not teacher:
        raise HTTPException(status_code=403, detail="Teacher access only")

    return teacher


# course ต้องเป็นของ teacher คนนี้ (ไม่เจอ = 404, ของคนอื่น = 403)
def get_own_course(db: Session, teacher: Teacher, course_code: int):
    course = db.query(Course).filter(Course.course_code == course_code, Course.is_deleted == False).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.teacher_id != teacher.teacher_id:
        raise HTTPException(status_code=403, detail="Not your course")
    return course


def count_enrolled(db: Session, course_code: int):
    return db.query(Enrollment).filter(Enrollment.course_code == course_code, Enrollment.status == "active").count()

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
        # จำนวนนักศึกษาจาก enrollments (รวมคนที่ join เองแต่ยังไม่มีคะแนน)
        student_number = count_enrolled(db, c.course_code)

        sections = db.query(Enrollment.section).filter(
            Enrollment.course_code == c.course_code,
            Enrollment.status == "active",
            Enrollment.section.isnot(None),
            Enrollment.section != "",
        ).distinct().order_by(Enrollment.section).all()
        section = c.section or ", ".join(row.section for row in sections) or None
        courses_dash.append({
            "course_code": c.course_code,
            "course_name": c.course_name,
            "course_id": c.course_id,
            "number_student": student_number,
            "section":section,
            "join_code": c.join_code,
            "join_open": c.join_open
        })
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
            "full_mark": q.full_mark,
            "weight": q.weight,
            "is_publish": q.is_publish,
            
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
    all_score = db.query(Score, Enrollment.section).outerjoin(
        Enrollment,
        (Enrollment.student_id == Score.student_id)
        & (Enrollment.course_code == assignment.course_code),
    ).filter(Score.quiz_id == quiz_id, Score.is_deleted == False).all()
    for s, section in all_score:
        # ข้อมูลนักศึกษาสำหรับแสดงชื่อ/รูปโปรไฟล์ในหน้า Grade
        stu = s.student
        student_score.append({
                "score_id": s.score_id,
                "score": s.score,
                "unread_flag": s.unread_flag,
                "section": section or assignment.course.section,
                "stu_id": s.student_id,
                "stu_fname": stu.first_name if stu else None,
                "stu_mname": stu.middle_name if stu else None,
                "stu_lname": stu.last_name if stu else None,
                "avatar_url": stu.avatar_url if stu else None
            })
    return {
        "assignment":{
            "assign_id": assignment.quiz_id,
            "assign_name": assignment.quiz_name,
            "is_publish": assignment.is_publish,
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

# รายชื่อนักศึกษาในวิชา + join code
@router.get("/course/{course_code}/roster")
async def course_roster(course_code: int, db: Session = Depends(get_db), current_user: AuthUser = Depends(get_current_user)):
    teacher = is_teacher(db, current_user)
    course = get_own_course(db, teacher, course_code)
    enrollments = db.query(Enrollment).filter(Enrollment.course_code == course_code, Enrollment.status == "active").order_by(Enrollment.student_id).all()
    students = []
    for e in enrollments:
        stu = e.student
        students.append({
            "student_id": e.student_id,
            "first_name": stu.first_name,
            "middle_name": stu.middle_name,
            "last_name": stu.last_name,
            "email": stu.auth_user.email if stu.auth_user else None,
            "avatar_url": stu.avatar_url,
            "section": e.section or course.section,
            "joined_via": e.joined_via,
            # ถูกเพิ่มผ่าน CSV สมัยก่อนแต่ยังไม่ได้สมัครบัญชี
            "signed_up": bool(stu.auth_user and stu.auth_user.password),
            "joined_at": e.created_at,
        })
    return {
        "course": {
            "course_code": course.course_code,
            "course_name": course.course_name,
            "course_id": course.course_id,
            "join_code": course.join_code,
            "join_open": course.join_open,
        },
        "students": students,
    }

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
            course_id=course.course_id,
            section=course.section,
            join_code=generate_join_code(db)
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
async def create_assignments(assign: Assignment,db: Session= Depends(get_db),current_user: AuthUser = Depends(get_current_user)):
    try:
        teacher = is_teacher(db,current_user)

        new_assignment = Quiz(
            quiz_name=assign.quiz_name,
            full_mark=assign.full_mark,
            course_code=assign.course_code,
            weight=assign.weight
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
# คอลัมน์ที่ต้องมี: student_id, student_email, score, section (name ไม่บังคับ)
# ไม่สร้างบัญชีให้แล้ว — คนที่ยังไม่มีบัญชีจะอยู่ใน unmatched ให้อาจารย์อัปโหลดซ้ำหลังนักศึกษาสมัคร
CSV_REQUIRED_COLUMNS = {"student_id", "student_email", "score", "section"}

@router.post("/upload/{course_code}/{quiz_id}")
async def upload_csv(quiz_id: str,course_code: int,file: UploadFile = File(...),db: Session = Depends(get_db),current_user: AuthUser = Depends(get_current_user)):
    teacher = is_teacher(db, current_user)
    assignment = db.query(Quiz).join(Course).filter(Quiz.quiz_id == quiz_id,Quiz.course_code == course_code,Course.teacher_id==teacher.teacher_id).first()
    if not assignment:
        raise HTTPException(status_code=404,detail="assignment not found")

    # อ่านละแปลงเป็นข้อความ -> ตาราง
    try:
        decoded = (await file.read()).decode("utf-8-sig")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400,detail="Upload failed: file must be UTF-8 CSV")
    reader = csv.DictReader(io.StringIO(decoded), delimiter=',')
    missing = CSV_REQUIRED_COLUMNS - set(reader.fieldnames or [])
    if missing:
        raise HTTPException(status_code=400,detail=f"Upload failed: missing columns {', '.join(sorted(missing))}")

    rows = []
    for line_no, row in enumerate(reader, start=2):
        stu_id = str(row["student_id"] or "").strip()
        if not stu_id:
            continue
        try:
            score_v = float(row["score"])
        except (TypeError, ValueError):
            raise HTTPException(status_code=400,detail=f"Upload failed: invalid score on line {line_no}")
        rows.append({
            "student_id": stu_id,
            "email": str(row["student_email"] or "").strip(),
            "name": str(row.get("name") or "").strip(),
            "score": score_v,
            "section": str(row["section"] or "").strip() or None,
        })

    try:
        # ถ้ามีการ upload อีกครั้ง ก็ให้ยัง ไม่publish ต้องกดอีกครั้งถึงจะ publish
        if assignment.is_publish:
            assignment.is_publish = False
        db.add(Upload(file_name=file.filename, teacher_id=teacher.teacher_id, course_code=assignment.course_code))

        ids = [r["student_id"] for r in rows]
        stu_index = {s.student_id: s for s in db.query(Student).filter(Student.student_id.in_(ids)).all()}
        score_index = {s.student_id: s for s in db.query(Score).filter(Score.student_id.in_(ids),Score.quiz_id==quiz_id).all()}
        enroll_index = {e.student_id: e for e in db.query(Enrollment).filter(Enrollment.student_id.in_(ids),Enrollment.course_code==assignment.course_code).all()}

        matched = 0
        unmatched = []
        for r in rows:
            stu = stu_index.get(r["student_id"])
            # ต้องมีบัญชีแล้ว และ email ใน CSV ต้องตรงกับบัญชี (กันใส่รหัสผิดคน)
            if not stu:
                unmatched.append({**r, "reason": "not_registered"})
                continue
            if not stu.auth_user or stu.auth_user.email.lower() != r["email"].lower():
                unmatched.append({**r, "reason": "email_mismatch"})
                continue
            matched += 1

            t_score = score_index.get(r["student_id"])
            if t_score:
                # Update คะแนนเดิม
                t_score.score = r["score"]
                t_score.unread_flag = True
                t_score.is_deleted = False
            else:
                # สร้างคะแนนใหม่
                t_score = Score(score=r["score"], quiz_id=quiz_id, student_id=r["student_id"])
                db.add(t_score)
                score_index[r["student_id"]] = t_score

            # อาจารย์อัปโหลดคะแนนให้ = อยู่ในวิชา (ถ้าเคยถูกเอาออกก็กลับมา active)
            enrollment = enroll_index.get(r["student_id"])
            if enrollment:
                enrollment.status = "active"
                if r["section"]:
                    enrollment.section = r["section"]
            else:
                enrollment = Enrollment(student_id=r["student_id"], course_code=assignment.course_code, section=r["section"], status="active", joined_via="csv")
                db.add(enrollment)
                enroll_index[r["student_id"]] = enrollment
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,detail=f"Upload failed: {str(e)}")

    for u in unmatched:
        u.pop("score", None)
    return {"message": "CSV uploaded successfully", "matched": matched, "unmatched": unmatched}

############################################################################ enrollment ##################################################################
# สร้าง join code ใหม่ (code เก่าใช้ไม่ได้ นักศึกษาที่ join แล้วยังอยู่)
@router.post("/course/{course_code}/join_code/regenerate")
async def regenerate_join_code(course_code: int, db: Session = Depends(get_db), current_user: AuthUser = Depends(get_current_user)):
    teacher = is_teacher(db, current_user)
    course = get_own_course(db, teacher, course_code)
    course.join_code = generate_join_code(db)
    db.commit()
    return {"join_code": course.join_code, "join_open": course.join_open}

# เปิด/ปิดรับนักศึกษา
@router.post("/course/{course_code}/join_code/toggle")
async def toggle_join(course_code: int, db: Session = Depends(get_db), current_user: AuthUser = Depends(get_current_user)):
    teacher = is_teacher(db, current_user)
    course = get_own_course(db, teacher, course_code)
    course.join_open = not course.join_open
    db.commit()
    return {"join_code": course.join_code, "join_open": course.join_open}

# เอานักศึกษาออกจากวิชา (soft: status = dropped, คะแนนยังอยู่)
@router.post("/course/{course_code}/remove/{student_id}")
async def remove_student(course_code: int, student_id: str, db: Session = Depends(get_db), current_user: AuthUser = Depends(get_current_user)):
    teacher = is_teacher(db, current_user)
    get_own_course(db, teacher, course_code)
    enrollment = db.query(Enrollment).filter(Enrollment.course_code == course_code, Enrollment.student_id == student_id, Enrollment.status == "active").first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Student not enrolled in this course")
    enrollment.status = "dropped"
    db.commit()
    return {"message": "Student removed"}

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

@router.post("/update_course/{course_code}")
async def update_course(course_code: int, course_data: CourseUpdate, db: Session = Depends(get_db), current_user: AuthUser = Depends(get_current_user)):
    try:
        teacher = is_teacher(db, current_user)
        course = db.query(Course).filter(Course.course_code == course_code, Course.teacher_id == teacher.teacher_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        course.course_name = course_data.course_name
        course.course_id = course_data.course_id
        db.commit()
        return {"message": "Course updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"error: {str(e)}")

@router.post("/update_assign/{assign_id}")
async def update_assignment(assign_id: str, assign_data: AssignmentUpdate, db: Session = Depends(get_db), current_user: AuthUser = Depends(get_current_user)):
    try:
        teacher = is_teacher(db, current_user)
        assignment = db.query(Quiz).join(Course).filter(Quiz.quiz_id == assign_id, Course.teacher_id == teacher.teacher_id).first()
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")
        
        assignment.quiz_name = assign_data.quiz_name
        assignment.full_mark = assign_data.full_mark
        assignment.weight = assign_data.weight
        db.commit()
        return {"message": "Assignment updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"error: {str(e)}")
