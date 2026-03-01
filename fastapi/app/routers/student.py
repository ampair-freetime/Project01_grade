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
#!/usr/bin/env python3
# fastapi/app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import distinct
from app.db import get_db
from app.models import Student, Score, Quiz, Course
from app.routers.auth import get_cerrent_user
from app.models.authuser import AuthUser
from app.config import settings
from jose import jwt, JWTError
from datetime import datetime, timedelta
from httpx import AsyncClient