from fastapi import APIRouter
from app.db import get_db
router = APIRouter()

@router.get("/dashboard_student")
async def stu_dashboard():
    #นำค่า courses มาแสดงผลในหน้า student/dashboard
    return ...

@router.get("/courses")
async def stu_courses():
    #นำ งานใน courses นั้นๆมาแสดงผล
    return ...

@router.get("/score")
async def stu_scores():
    #นำคะแนนมาแสดงผลพร้อมคำนวณ std mean median highest lowest จาก ใน sec นั้นๆ
    return ...