# fastapi/app/models/__init__.py

# authuser (ข้อมูลผู้ใช้/role)
from .authuser import AuthUser
# courses (ตารางรายวิชา)
from .courses import Course
# student (นักเรียน)
from .student import Student
# teacher (อาจารย์)
from .teacher import Teacher
# score (คะแนน)
from .scores import Score
# uploads (อัปโหลด)
from .uploads import Upload
# quiz (ควิซ)
from .quiz import Quiz
# authprovider (จัดการการล็อกอิน)
from .authprovider import AuthProvider