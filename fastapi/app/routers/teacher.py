from fastapi import APIRouter
from app.db import get_db

router = APIRouter()

@router.get("/dashboard_teacher")
async def teacher_dashboard():
    #คืนค่าวิชาที่อาจารย์สอน
    return ...

@router.post("/create_course")
async def create_courses():
    # สร้าง courses ของ อาจารย์
    return ...

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

# @router ในการ ดึงข้อมูล csv มาทำใส่ database
@router.post("/upload")
async def upload_csv():
    return ...