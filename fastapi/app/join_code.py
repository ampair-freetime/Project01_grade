# สร้าง join code ของวิชา (ใช้ alphabet เดียวกับ demo: ไม่มี 0/O/1/I กันอ่านสับสน)
import secrets
from sqlalchemy.orm import Session
from app.models.courses import Course

JOIN_CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
JOIN_CODE_LENGTH = 6


def generate_join_code(db: Session) -> str:
    # 32^6 ≈ 1 พันล้านแบบ ชนกันยากมาก แต่เช็คซ้ำไว้ก่อน
    while True:
        code = "".join(secrets.choice(JOIN_CODE_ALPHABET) for _ in range(JOIN_CODE_LENGTH))
        if not db.query(Course).filter(Course.join_code == code).first():
            return code
