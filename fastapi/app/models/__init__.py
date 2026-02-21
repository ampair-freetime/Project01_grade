# fastapi/app/models/__init__.py

# authuser (ข้อมูลผู้ใช้/role)
from .authuser import AuthUser
# courses (ตารางรายวิชา)
from .courses import Course
# enrollments (ตารางคะแนน)
from .enrollments import Enrollment
# student (นักเรียน)
from .student import Student
# teacher (อาจารย์)
from .teacher import Teacher