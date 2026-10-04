# ชุดทดสอบกลาง: ระบบประกาศคะแนนสอบ — ทีม 4 คน

อ้างอิงข้อ 3 ใน Project-Final-Report-DB-1-69.pdf และโค้ดปัจจุบันใน fastapi/app/ กับ frontend/src/
ข้อมูลทั้งหมดเป็นข้อมูลสมมติสำหรับสาธิต ไม่ใช่บัญชีมหาวิทยาลัยจริง ไม่ต้องส่งอีเมลหรือเข้า Google ด้วยบัญชีเหล่านี้
ชุดนี้เตรียมข้อมูลและผลที่คาดหวัง ยังไม่ได้รันทดสอบกับฐานข้อมูลจริง

## 1. ข้อตกลงร่วมกัน

- ทั้ง 4 คนใช้ backend และฐานข้อมูลทดสอบเดียวกัน เดโมตามลำดับด้านล่าง
- ถ้าอัดแยกเครื่อง ให้ใช้ข้อมูลชุดเดียวกันและทำขั้นตอนก่อนหน้าจนถึงจุดรับช่วงของตน
- ใช้รหัสวิชา `DEMO321` เพียงรายการเดียวสำหรับอาจารย์บัญชีนี้ ถ้ามีหลายรายการต้องเลือก course_code ให้ชัดก่อนตรวจผล
- `courses.course_code` คือ PK ตัวเลขที่ระบบสร้าง; `courses.course_id` คือรหัสวิชา `DEMO321` ที่กรอกบน UI
- ห้ามกำหนด UUID, course_code หรือ join_code เอง ให้จดค่าจริงที่ระบบสร้างในตารางรับช่วง
- ใช้ชื่อและค่าตามเอกสารนี้ ห้ามเปลี่ยนคะแนนระหว่างการอัด เพราะผลสถิติจะเปลี่ยน
- สมัครนักศึกษาทั้ง 5 คนให้เสร็จก่อนอัปโหลด CSV; CSV ไม่ได้สร้างบัญชีให้อัตโนมัติ
- รหัสผ่านสมมติทุกบัญชี: `DemoScore69!` ช่อง Confirm Password ใช้ค่าเดียวกัน Middle Name เว้นว่าง
- ใช้ตัวพิมพ์เล็กของ email ตามไฟล์ เพราะ login ปัจจุบันเทียบ email แบบตรงตัว
- ไม่ต้องนำ accounts.csv ไปอัปโหลดคะแนน ไฟล์นี้เป็นโพยสำหรับกรอกหน้า Sign up เท่านั้น
- เปิดอาจารย์และนักศึกษาในคนละ browser/profile เพื่อไม่ให้ cookie ของอีกบัญชีทับกัน
- ภาพหลักฐานต้องจับจาก PostgreSQL จริง ไฟล์ verify.sql ใช้ตรวจผล ไม่ใช่ SQL ที่ backend ส่งทั้งหมด

## 2. บัญชีทดสอบ

| บทบาท | First Name | Last Name | Student ID | Email | การเตรียม |
|---|---|---|---|---|---|
| อาจารย์ | Demo | Teacher | เว้นว่าง | demo.teacher@cmu.ac.th | สมัครก่อนอัด |
| นักศึกษา 1 | Demo | One | 690510901 | demo_one@cmu.ac.th | สมัครก่อนอัด |
| นักศึกษา 2 | Demo | Two | 690510902 | demo_two@cmu.ac.th | สมัครก่อนอัด |
| นักศึกษา 3 | Demo | Three | 690510903 | demo_three@cmu.ac.th | สมัครสดโดยคนที่ 1 |
| นักศึกษา 4 | Demo | Four | 690510904 | demo_four@cmu.ac.th | สมัครก่อนอัด |
| นักศึกษา 5 | Demo | Five | 690510905 | demo_five@cmu.ac.th | สมัครก่อนอัด |

อีเมลอาจารย์ใช้จุด `.` และอีเมลนักศึกษาใช้ `_` เพื่อให้ตรงกับเงื่อนไขแยกบทบาทในระบบ
บัญชีตัวหลักที่นักศึกษาล็อกอินในการเดโมคือ `demo_three@cmu.ac.th`

## 3. ข้อมูลวิชาและงาน

| รายการ | ค่า |
|---|---|
| Course ID ที่กรอกบน UI | DEMO321 |
| Course Name ตอนสร้าง | Database Demo |
| Course Name หลังแก้ไข | Database Systems Demo |
| Section | 001 |
| อาจารย์เจ้าของ | Demo Teacher |
| งานหลัก | Midterm |
| คะแนนเต็มงานหลัก | 100 |
| Weight งานหลัก | 100 (กรอก 100 ไม่ใช่ 1) |
| งานสำหรับทดสอบลบ | Practice Delete |
| คะแนนเต็มงานลบ | 20 |
| Weight งานลบ | 10 |

สร้างงานลบเฉพาะช่วงคนที่ 4 และไม่ Publish งานนี้ จึงไม่กระทบค่าเฉลี่ยถ่วงน้ำหนักงานหลัก

## 4. ไฟล์คะแนนและผลลัพธ์กลาง

CSV เป็น UTF-8 ใช้ comma และมีหัว `student_id,student_email,score,section,name`
คอลัมน์ name เป็นข้อมูลประกอบ ไม่ใช่การแก้ชื่อบัญชี คอลัมน์ section ลงใน enrollments ไม่ใช่ scores

| Student ID | ชื่อ | Midterm ครั้งแรก | หลังแก้ไข | อันดับหลังแก้ |
|---|---|---:|---:|---:|
| 690510901 | Demo One | 60 | 60 | 5 |
| 690510902 | Demo Two | 70 | 70 | 4 |
| 690510903 | Demo Three | 80 | 85 | 3 |
| 690510904 | Demo Four | 90 | 90 | 2 |
| 690510905 | Demo Five | 100 | 100 | 1 |

- `midterm_initial.csv`: นำเข้า Midterm ครั้งแรก ได้ matched = 5, unmatched = []
- `midterm_updated.csv`: นำเข้าทับ Midterm เดิม เปลี่ยนเฉพาะ Demo Three จาก 80 เป็น 85; ยังมี 5 แถวคะแนน ไม่ใช่ 10
- `practice_delete.csv`: นำเข้า Practice Delete เท่านั้น Demo Three ได้ 15/20

| ตัวชี้วัด Midterm | ก่อนแก้ไข | หลังแก้ไข |
|---|---:|---:|
| จำนวนผู้มีคะแนน | 5 | 5 |
| Mean | 80.00 | 81.00 |
| Median | 80.00 | 85.00 |
| Population Std | 14.14 | 14.28 |
| Highest / Lowest | 100 / 60 | 100 / 60 |
| คะแนน Demo Three | 80/100 | 85/100 |
| Percent Demo Three | 80.00% | 85.00% |
| Rank Demo Three | 3/5 | 3/5 |
| Weighted Average Demo Three เมื่อมีแค่ Midterm ที่ Publish | 80.00 | 85.00 |

Std ใช้สูตรหารด้วย N ตรงกับ backend ไม่ใช่ sample standard deviation

## 5. ลำดับรับผิดชอบทั้ง 4 คน (เปลี่ยนผู้รับผิดชอบได้ แต่คงลำดับ)

เวลาเป้าหมายรวม 9:40 นาที ทุกคนแนะนำตอนเรียน รหัส ชื่อ-สกุล และเห็นหน้าขณะนำเสนอ
ตอนเรียนให้ใส่ค่าจริง เพราะ README โปรเจกต์ไม่ได้ระบุไว้

### เปิดคลิป 0:00–0:40 — ทุกคน

ชื่อโครงงาน ระบบประกาศคะแนนสอบ กลุ่ม G12 แล้วแนะนำตัวคนละประมาณ 8 วินาที

### คนที่ 1: ชฎาภา อนุกูลเรืองรุ่ง — 670510698 (0:40–2:30)

หน้าจอ: Sign up → Login → Teacher Courses

1. สมัคร Demo Three ด้วยข้อมูลบัญชีด้านบน
   - คาดหวัง: สมัครสำเร็จ เกิดแถว auth_users และ students ที่เชื่อมกัน
   - Capture A01: ฟอร์ม/ผลสำเร็จ + SQL จริง + ผล verify.sql ส่วน A (ไม่แสดง password hash)
2. Login อาจารย์ด้วย demo.teacher@cmu.ac.th / DemoScore69!
   - คาดหวัง: เข้าหน้า Teacher Courses
   - Capture A02: หน้า login/ผลปลายทาง + SQL lookup ผู้ใช้จริงที่ใช้ตรวจบัญชี
3. สร้าง DEMO321 / Database Demo / Section 001
   - คาดหวัง: มีแถว courses ใหม่ join_open = true, is_deleted = false, is_archive = false
   - Capture A03: ฟอร์ม/การ์ดวิชา + SQL จริง + verify.sql ส่วน B
4. แก้ชื่อวิชาเป็น Database Systems Demo โดยคง Course ID DEMO321
   - Capture A04: ชื่อก่อน–หลังบน UI และแถว courses หลังเปลี่ยน
5. ส่ง course_code และ join_code จริงให้คนที่ 2

คำพูดหลัก: “ระบบแยกบัญชีอาจารย์กับนักศึกษา และอาจารย์สร้างวิชาพร้อมรหัสเข้าร่วมให้ผู้เรียน”

### คนที่ 2: ฐิติพันธ์ วงศ์สุรดาพร — 670510703 (2:30–4:15)

หน้าจอ: Student Dashboard + Join dialog → Student Course Detail

1. Login Demo Three แล้วเปิด Dashboard ก่อนเข้าร่วม
   - ถ้าบัญชีใหม่จริง คาดหวัง: ยังไม่มีวิชา DEMO321
2. กรอก join_code ที่คนที่ 1 ส่งให้ ตรวจชื่อวิชาและ Section 001 แล้วกดยืนยัน
   - คาดหวัง: enrollments ของ 690510903 มี status = active, joined_via = code
   - enrollment.section ตอน join อาจเป็น NULL; UI แสดง 001 จากค่า courses.section
   - Capture B01: join preview/ผลบน Dashboard + SQL จริง + verify.sql ส่วน C
3. เปิด Course Detail ก่อนมีคะแนนประกาศ
   - คาดหวัง: เห็นวิชาและอาจารย์ แต่ assessments ว่าง Weighted Average = 0
   - Capture B02: UI ที่ไม่มีคะแนน + SQL SELECT จริง
4. ส่งต่อสถานะ “นักศึกษา 3 เข้าร่วมแล้ว ยังไม่มีคะแนน” ให้คนที่ 3

คำพูดหลัก: “ข้อมูลการเข้าร่วมถูกเก็บแยกจากคะแนน นักศึกษาจึงเห็นรายวิชาได้แม้ยังไม่ถูกให้คะแนน”

### คนที่ 3: นภิสา ศรีทุมมา — 670510711 (4:15–6:50)

หน้าจอ: Teacher Assignment Management → Teacher Grade

1. Login อาจารย์ เปิดวิชาเดียวกัน สร้าง Midterm / Full Mark 100 / Weight 100
   - คาดหวัง: quizzes มี Midterm, is_publish = false
   - Capture C01: งานใหม่ + SQL จริง + verify.sql ส่วน D
2. เปิด Grade ของ Midterm อัปโหลด midterm_initial.csv
   - คาดหวัง: 5 คน คะแนน 60,70,80,90,100; unread_flag ทุกคน = true
   - enrollments รวม 5 active: Demo Three joined_via = code; อีก 4 คน joined_via = csv
   - enrollment.section ทุกคน = 001; uploads มีชื่อไฟล์ที่นำเข้า
   - Capture C02: ผลนำเข้า/UI คะแนน + SQL จริง + verify.sql ส่วน C/E/F
3. Publish Midterm ครั้งแรก
   - คาดหวัง: quizzes.is_publish = true
   - Capture C03: UI หลังประกาศ + SQL UPDATE จริง + verify.sql ส่วน D
4. อัปโหลด midterm_updated.csv ที่งาน Midterm เดิม
   - คาดหวัง: Demo Three = 85; score_id เดิม; จำนวนคะแนนยัง 5; is_publish กลับเป็น false
   - ทุกแถวที่ matched ถูกตั้ง unread_flag = true อีกครั้ง แม้ตัวเลขคะแนนบางคนไม่เปลี่ยน
   - Capture C04: คะแนน 80→85 + จำนวนแถว/score_id ก่อน–หลัง + is_publish = false
5. กด Publish อีกครั้งก่อนส่งต่อคนที่ 4
   - Capture C05: is_publish = true + verify.sql ส่วน G (สถิติหลังแก้)

คำพูดหลัก: “อัปโหลดซ้ำแก้คะแนนเดิม และระบบยกเลิกสถานะประกาศเพื่อให้อาจารย์ตรวจแล้วประกาศใหม่”

### คนที่ 4: ศุภาการ แก้วพวงใหม่ — 670510728 (6:50–9:20)

หน้าจอ: Student Course Detail → Student Score → Teacher Assignment/Grade

1. Login Demo Three เปิด Course Detail ใหม่
   - คาดหวัง: เห็น Midterm; Weighted Average 85.00; unread_flag ก่อนเปิด Score = true
   - Capture D01: UI และผล SELECT จริง
2. เปิด Score ของ Midterm
   - คาดหวัง: 85/100, 85%, Rank 3/5, Mean 81, Median 85, Std 14.28, High 100, Low 60
   - เกิด UPDATE unread_flag ของ Demo Three เป็น false; ของอีก 4 คนยัง true
   - Capture D02: UI คะแนน/สถิติ + SQL จริง + verify.sql ส่วน E/G
3. สลับ browser อาจารย์ สร้าง Practice Delete / Full Mark 20 / Weight 10 แล้วนำเข้า practice_delete.csv
   - คาดหวัง: มีคะแนน Demo Three = 15 และงานนี้ไม่ Publish
4. ลบคะแนน Demo Three จาก Practice Delete
   - คาดหวัง: scores.is_deleted = true; Query รายการคะแนน active ไม่พบแถวนั้น
   - Capture D03: UI ก่อน–หลัง + SQL UPDATE จริง + verify.sql ส่วน H
5. ลบงาน Practice Delete
   - คาดหวัง: quizzes.is_deleted = true; ไม่ปรากฏในรายการงาน active; Midterm ยังอยู่
   - Capture D04: UI ก่อน–หลัง + SQL UPDATE จริง + verify.sql ส่วน H

คำพูดหลัก: “นักศึกษาดูคะแนนตนเองพร้อมสถิติ และเมื่อเปิดอ่าน ระบบบันทึกสถานะให้อาจารย์เห็น การลบเป็น Soft delete”

### ปิดคลิป 9:20–9:40 — คนที่ 4

สรุปว่าระบบจัดการวิชา รับคะแนนจาก CSV ประกาศคะแนน และให้นักศึกษาดูผลได้

## 6. ตารางรับช่วง (เติมค่าจริงร่วมกัน)

| ค่า | ค่าจริงจากการรัน |
|---|---|
| URL frontend / backend ที่ทุกคนใช้ | ... |
| ฐานข้อมูลทดสอบ | ... |
| teacher_id ของ demo.teacher | ... |
| course_code ของ DEMO321 | ... |
| join_code ของ DEMO321 | ... |
| quiz_id ของ Midterm | ... |
| score_id ของ Demo Three ใน Midterm ก่อนแก้ | ... |
| score_id ของ Demo Three ใน Midterm หลังแก้ (ต้องเท่ากัน) | ... |
| quiz_id ของ Practice Delete | ... |
| ตอนเรียนจริงของสมาชิกแต่ละคน | ... |

## 7. เคสเสริมสำหรับซ้อม/ตอบคำถาม (ทำหลังอัดเส้นหลัก)

ใช้ Midterm ที่ยังไม่ Publish หรือสร้างงาน QA แยก เพราะการนำเข้า CSV ที่ parse ผ่านจะบันทึก uploads และอาจเปลี่ยน is_publish แม้ matched = 0

| เคส | ข้อมูล/การกระทำ | ผลที่คาดหวังตามโค้ด |
|---|---|---|
| รหัสผ่านผิด | demo_three@cmu.ac.th / WrongPassword1! | Login ไม่สำเร็จ HTTP 401 |
| สมัคร email ซ้ำ | ข้อมูล Demo Three เดิม | ไม่สร้างบัญชีเพิ่ม HTTP 409 |
| Student ID ซ้ำกับ email ใหม่ | 690510903 / demo_duplicate@cmu.ac.th | HTTP 409 ไม่เพิ่ม students |
| ขาดหัว section | error_missing_column.csv | HTTP 400 missing columns section; ไม่บันทึก upload |
| คะแนนไม่ใช่ตัวเลข | error_invalid_score.csv | HTTP 400 invalid score on line 2; ไม่บันทึก upload |
| Email ไม่ตรง ID | error_email_mismatch.csv | matched = 0, unmatched มี reason email_mismatch; คะแนนไม่เปลี่ยน |
| ยังไม่สมัคร | error_not_registered.csv | matched = 0, unmatched มี reason not_registered; ไม่สร้างบัญชี/คะแนน |
| ปิดรับเข้าร่วม | ปิด join_open แล้วลอง join ด้วยนักศึกษาที่ยังไม่เข้าวิชา | เข้าร่วมไม่ได้ เปิดรับคืนเมื่อทดสอบเสร็จ |
| ออกรายวิชาโดยอาจารย์ | Remove Demo Five | enrollment.status = dropped; กลับเข้าร่วมได้เมื่อเปิดรับ |
| Archive/Restore | Archive DEMO321 แล้ว Restore | is_archive true→false; กลับมาใน Dashboard อาจารย์ |
| ลบวิชา | สร้างวิชา DEMO321-DELETE แล้วลบ | is_deleted = true; ไม่ลบ DEMO321 หลัก |

ไม่กำหนดเคส “คะแนนติดลบ/เกินเต็มต้องถูกปฏิเสธ” ว่าผ่านแน่นอน เพราะโค้ด CSV ปัจจุบันยังไม่ได้ตรวจช่วงคะแนน
การไม่เห็นงานยังไม่ Publish บนหน้า Course Detail เป็นพฤติกรรมหน้า UI; เอกสารนี้ไม่ได้รับรองการป้องกันเข้าถึงผ่าน URL โดยตรง

## 8. SQL และหลักฐานที่ต้องเตรียม

เปิด verify.sql ใน pgAdmin Query Tool และรันแต่ละส่วน ณ จังหวะที่เอกสารระบุ แสดงชื่อคอลัมน์และ record ที่ตรวจ
ส่วน SQL ที่ระบบใช้ให้เก็บจาก log/SQL trace ระหว่างกด UI จริง พร้อม parameters ที่เป็นข้อมูลสมมติ
SQLAlchemy จะส่งหลายคำสั่ง โดยเฉพาะสมัครสมาชิกและ CSV อย่าอ้างว่าตัวอย่าง SQL ด้านล่างเป็น trace จริงครบทุกคำสั่ง

ตัวอย่าง SQL เทียบเท่าสำหรับอธิบาย (แทน :... ด้วยค่าจริงเฉพาะถ้าต้องใช้; ไม่ต้องรันซ้ำเพื่อเดโม):

```sql
-- แก้ชื่อวิชา
UPDATE courses SET course_name = 'Database Systems Demo'
WHERE course_code = :course_code;
-- แก้คะแนน (การอัปโหลดจริงยังอัปเดตแถวอื่นและ enrollment ด้วย)
UPDATE scores SET score = 85, unread_flag = true, is_deleted = false,
                  updated_at = CURRENT_TIMESTAMP
WHERE quiz_id = :midterm_id AND student_id = '690510903';
-- Publish
UPDATE quizzes SET is_publish = true WHERE quiz_id = :midterm_id;
-- เปิดอ่าน
UPDATE scores SET unread_flag = false
WHERE quiz_id = :midterm_id AND student_id = '690510903';
-- Soft delete คะแนนทดลอง
UPDATE scores SET is_deleted = true, updated_at = CURRENT_TIMESTAMP
WHERE quiz_id = :practice_id AND student_id = '690510903';
-- Soft delete งานทดลอง
UPDATE quizzes SET is_deleted = true WHERE quiz_id = :practice_id;
```

หลักฐานลบต้องแสดง 2 ภาพ: แถวจริงที่มี is_deleted = true และผล SELECT active ที่ไม่ปรากฏแถวนั้น
หน้า Score ต้องจับก่อน–หลัง unread_flag อย่าเปิด Score ล่วงหน้าก่อน Capture ค่า true

## 9. ซ้อมและอัดซ้ำ

- ก่อนซ้อมตรวจทุกบัญชีว่ามี First/Last Name และ email/ID ตรง CSV; หลีกเลี่ยงการแก้ CSV ผ่าน Excel ที่ทำ section 001 กลายเป็น 1
- ใช้ฐานข้อมูลทดสอบสะอาดสำหรับการอัดเต็มรอบใหม่ โดยเลือกสภาพเริ่มต้นเดียวกับหัวข้อ 2
- ถ้าทำซ้ำในฐานเดิม อย่าสมัครบัญชีหรือสร้าง DEMO321/Midterm ซ้ำ; ข้ามส่วนที่มีแล้วหรือใช้ฐานทดสอบแยกรอบ
- อัปโหลด midterm_initial.csv ซ้ำช่วยคืนคะแนน แต่ไม่คืนสถานะ enrollment/บัญชี/วิชาให้เหมือนเริ่มต้นทั้งหมด
- ถ้าต้องการคืน unread_flag เป็น true สำหรับซ้อมหน้า Score ให้อัปโหลดไฟล์คะแนนอีกครั้งและ Publish ใหม่
- ทดสอบเคสเสริมหลังเก็บวิดีโอเส้นหลักเพื่อไม่ให้จำนวนผู้เรียนและสถิติผิดจากตาราง
- ก่อนส่งตรวจวิดีโอไม่เกิน 10 นาที เห็นหน้าผู้นำเสนอทั้ง 4 คน และมีตัวอย่างทุกหน้าจอในขอบเขตงาน
