## Team: (25cs212g12) ท้ายcomsci 📍  
### Project: 2 ประกาศคะแนนสอบ
**Group ID:** 25cs212g12
**Mentor:** กนิษฐา บุตรชุมแสง (พี่เนย)  

### Tech Stack:
- **Frontend:** Vue, Tailwind CSS, HTML5, CSS, JavaScript  
- **Backend:** FastAPI
### Members:

#### 1. ชฎาภา อนุกูลเรืองรุ่ง
- **Student ID:** 670510698 
- **GitHub ID:** [4whalelocirapter](https://github.com/4whalelocirapter)  
- **Role:** Backend

#### 2. ฐิติพันธ์ วงศ์สุรดาพร
- **Student ID:** 670510703  
- **GitHub ID:** [thitiphanw](https://github.com/thitiphanw)  
- **Role:** Frontend

#### 3. นภิสา ศรีทุมมา
- **Student ID:** 670510711  
- **GitHub ID:** [toraon-tonaor](https://github.com/toraon-tonaor)  
- **Role:** Frontend  

#### 4. ศุภาการ แก้วพวงใหม่
- **Student ID:** 670510728  
- **GitHub ID:** [ampair-freetime](https://github.com/ampair-freetime) 
- **Role:** Backend 

---

### Notes:
- Note  

### Database migration: section stored in enrollment

Student-specific sections are stored in `enrollments`. CSV uploads still accept
the `section` column, and score API responses read it from the student's course
enrollment, falling back to the optional course section set by the teacher.

For an existing PostgreSQL database, stop application workers and run with the
backend's configured database environment:

```bash
cd fastapi
python migrate_score_section.py
```

Then start workers with the updated code. The migration creates missing
enrollments, preserves existing nonblank enrollment sections, fills missing
sections from the latest nonblank legacy score section, and drops `scores.section`.
It can be rerun. New databases created from the models have no score section column.

### Course section field

Teachers can set an optional section when creating a course. Students see it in
the join preview, dashboard, and course details. An enrollment section supplied
through CSV takes precedence over this course default.

For an existing database, run `python migrate_course_section.py` from `fastapi/`
before starting the updated backend. This migration can be rerun and is also
included in `migrate_enrollment.py`.
