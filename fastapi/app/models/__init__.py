# fastapi/app/models/__init__.py

# เพิ่ม UserRole ต่อท้าย AuthUser
from .authuser import AuthUser, UserRole
from .courses import Course
from .enrollments import Enrollment