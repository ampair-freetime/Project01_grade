# ข้อมูลและแผนนำเสนอระบบประกาศคะแนนสอบ — กลุ่ม G12

อ้างอิงข้อ 3 ใน Project-Final-Report-DB-1-69.pdf และโค้ดปัจจุบันใน fastapi/app/ กับ frontend/src/
ชื่อสมาชิกผู้นำเสนออ้างอิง README ของโครงงาน ส่วนชื่ออาจารย์ นักศึกษา อีเมล และบัญชีใช้งานด้านล่างเป็นข้อมูลสมมติที่ตั้งให้เหมือนการใช้งานในรายวิชา ไม่ใช่ข้อมูลผู้ใช้จริง
เอกสารนี้รวมภาพรวม บัญชี ข้อมูลรายวิชา คะแนน CSV ทุกชุด ลำดับของทั้ง 4 คน และ SQL ตรวจผลไว้ในไฟล์เดียว ตรวจความสอดคล้องของข้อมูลแล้ว แต่ยังไม่ได้รันทดสอบกับฐานข้อมูลจริง


## ภาพรวมที่ทุกคนใช้ร่วมกัน

เรื่องราว: อาจารย์กิตติพงศ์เปิดรายวิชา 204321 Database Systems ตอนเรียน 001 → ธนกฤตสมัครและเข้าร่วม → อาจารย์นำเข้าคะแนน Midterm ของนักศึกษา 5 คน → แก้คะแนนธนกฤต 80 เป็น 85 และประกาศใหม่ → นักศึกษาดูคะแนนพร้อมสถิติ → อาจารย์ลบคะแนนและแบบฝึกหัด ER Diagram ที่ไม่ใช้แล้ว

| ผู้รับผิดชอบ | ช่วงเวลา | บัญชีที่ใช้ | ผลที่ส่งต่อ |
|---|---|---|---|
| ชฎาภา | 0:40–2:30 | สมัครธนกฤต → Login อาจารย์ | วิชา 204321 พร้อม course_code และ join_code จริง |
| ฐิติพันธ์ | 2:30–4:15 | ธนกฤต | มี enrollment แบบ code ก่อนมีคะแนน |
| นภิสา | 4:15–6:50 | อาจารย์กิตติพงศ์ | Midterm ประกาศแล้ว คะแนนธนกฤต 85 ผู้มีคะแนนรวม 5 คน |
| ศุภาการ | 6:50–9:20 | ธนกฤต → อาจารย์กิตติพงศ์ | คะแนนอ่านแล้ว พร้อมหลักฐาน Soft delete แบบฝึกหัด |

เปิดคลิปและแนะนำสมาชิก 0:00–0:40; ปิดคลิป 9:20–9:40

เส้นทางหน้าจอครบ: Sign up → Login → Teacher Courses → Student Dashboard → Student Course Detail → Teacher Assignment Management → Teacher Grade → Student Score


## 1. ข้อตกลงร่วมกัน

- ทั้ง 4 คนใช้ backend และฐานข้อมูลทดสอบเดียวกัน เดโมตามลำดับด้านล่าง
- ถ้าอัดแยกเครื่อง ให้ใช้ข้อมูลชุดเดียวกันและทำขั้นตอนก่อนหน้าจนถึงจุดรับช่วงของตน
- ใช้รหัสวิชา `204321` เพียงรายการเดียวสำหรับอาจารย์บัญชีนี้ ถ้ามีหลายรายการต้องเลือก course_code ให้ชัดก่อนตรวจผล
- `courses.course_code` คือ PK ตัวเลขที่ระบบสร้าง; `courses.course_id` คือรหัสวิชา `204321` ที่กรอกบน UI
- ห้ามกำหนด UUID, course_code หรือ join_code เอง ให้จดค่าจริงที่ระบบสร้างในตารางรับช่วง
- ใช้ชื่อและค่าตามเอกสารนี้ ห้ามเปลี่ยนคะแนนระหว่างการอัด เพราะผลสถิติจะเปลี่ยน
- สมัครนักศึกษาทั้ง 5 คนให้เสร็จก่อนอัปโหลด CSV; CSV ไม่ได้สร้างบัญชีให้อัตโนมัติ
- รหัสผ่านสมมติทุกบัญชี: `GradeBook69!` ช่อง Confirm Password ใช้ค่าเดียวกัน Middle Name เว้นว่าง
- ใช้ตัวพิมพ์เล็กของ email ตามไฟล์ เพราะ login ปัจจุบันเทียบ email แบบตรงตัว
- CSV บัญชีในหัวข้อ 10.1 เป็นโพยกรอกหน้า Sign up ไม่ใช่ไฟล์อัปโหลดคะแนน
- เปิดอาจารย์และนักศึกษาในคนละ browser/profile เพื่อไม่ให้ cookie ของอีกบัญชีทับกัน
- ภาพหลักฐานต้องจับจาก PostgreSQL จริง SQL ในหัวข้อ 11 ใช้ตรวจผล ไม่ใช่ SQL ที่ backend ส่งทั้งหมด

## 2. บัญชีทดสอบ

| บทบาท | First Name | Last Name | Student ID | Email | การเตรียม |
|---|---|---|---|---|---|
| อาจารย์ | กิตติพงศ์ | วัฒนกุล | เว้นว่าง | kittipong.wat@cmu.ac.th | สมัครก่อนอัด |
| นักศึกษา 1 | ณัฐวุฒิ | ศรีสุข | 690510901 | nattawut_sri@cmu.ac.th | สมัครก่อนอัด |
| นักศึกษา 2 | พิมพ์ชนก | ใจดี | 690510902 | pimchanok_jai@cmu.ac.th | สมัครก่อนอัด |
| นักศึกษา 3 | ธนกฤต | วงศ์สุวรรณ | 690510903 | thanakrit_wong@cmu.ac.th | สมัครสดโดยคนที่ 1 |
| นักศึกษา 4 | ชนัญชิดา | อินทร์แก้ว | 690510904 | chananchida_in@cmu.ac.th | สมัครก่อนอัด |
| นักศึกษา 5 | ปวริศ | สุขเกษม | 690510905 | pawarit_suk@cmu.ac.th | สมัครก่อนอัด |

อีเมลอาจารย์ใช้จุด `.` และอีเมลนักศึกษาใช้ `_` เพื่อให้ตรงกับเงื่อนไขแยกบทบาทในระบบ
บัญชีตัวหลักที่นักศึกษาล็อกอินในการเดโมคือ `thanakrit_wong@cmu.ac.th`

## 3. ข้อมูลวิชาและงาน

| รายการ | ค่า |
|---|---|
| Course ID ที่กรอกบน UI | 204321 |
| Course Name ตอนสร้าง | Database System |
| Course Name หลังแก้ไข | Database Systems |
| Section | 001 |
| อาจารย์เจ้าของ | กิตติพงศ์ วัฒนกุล |
| งานหลัก | Midterm |
| คะแนนเต็มงานหลัก | 100 |
| Weight งานหลัก | 100 (กรอก 100 ไม่ใช่ 1) |
| งานสำหรับทดสอบลบ | แบบฝึกหัด ER Diagram |
| คะแนนเต็มงานลบ | 20 |
| Weight งานลบ | 10 |

สร้างแบบฝึกหัด ER Diagram เฉพาะช่วงคนที่ 4 และไม่ Publish งานนี้ จึงไม่กระทบค่าเฉลี่ยถ่วงน้ำหนักงานหลัก

ค่า Weight 100 ของ Midterm ใช้กับชุดข้อมูลนำเสนอนี้เพื่อให้มีงานที่ประกาศเพียงหนึ่งรายการ ไม่ได้อ้างว่าเป็นสัดส่วนคะแนนจริงของรายวิชา ระบบคำนวณ Weighted Average จากผลรวม Weight ของงานที่ Publish

## 4. ไฟล์คะแนนและผลลัพธ์กลาง

CSV เป็น UTF-8 ใช้ comma และมีหัว `student_id,student_email,score,section,name`
คอลัมน์ name เป็นข้อมูลประกอบ ไม่ใช่การแก้ชื่อบัญชี คอลัมน์ section ลงใน enrollments ไม่ใช่ scores

| Student ID | ชื่อ | Midterm ครั้งแรก | หลังแก้ไข | อันดับหลังแก้ |
|---|---|---:|---:|---:|
| 690510901 | ณัฐวุฒิ ศรีสุข | 60 | 60 | 5 |
| 690510902 | พิมพ์ชนก ใจดี | 70 | 70 | 4 |
| 690510903 | ธนกฤต วงศ์สุวรรณ | 80 | 85 | 3 |
| 690510904 | ชนัญชิดา อินทร์แก้ว | 90 | 90 | 2 |
| 690510905 | ปวริศ สุขเกษม | 100 | 100 | 1 |

- `midterm_scores.csv`: นำเข้า Midterm ครั้งแรก ได้ matched = 5, unmatched = []
- `midterm_scores_revised.csv`: นำเข้าทับ Midterm เดิม เปลี่ยนเฉพาะ ธนกฤต วงศ์สุวรรณ จาก 80 เป็น 85; ยังมี 5 แถวคะแนน ไม่ใช่ 10
- `er_diagram_scores.csv`: นำเข้า แบบฝึกหัด ER Diagram เท่านั้น ธนกฤต วงศ์สุวรรณ ได้ 15/20

| ตัวชี้วัด Midterm | ก่อนแก้ไข | หลังแก้ไข |
|---|---:|---:|
| จำนวนผู้มีคะแนน | 5 | 5 |
| Mean | 80.00 | 81.00 |
| Median | 80.00 | 85.00 |
| Population Std | 14.14 | 14.28 |
| Highest / Lowest | 100 / 60 | 100 / 60 |
| คะแนน ธนกฤต วงศ์สุวรรณ | 80/100 | 85/100 |
| Percent ธนกฤต วงศ์สุวรรณ | 80.00% | 85.00% |
| Rank ธนกฤต วงศ์สุวรรณ | 3/5 | 3/5 |
| Weighted Average ธนกฤต วงศ์สุวรรณ เมื่อมีแค่ Midterm ที่ Publish | 80.00 | 85.00 |

Std ใช้สูตรหารด้วย N ตรงกับ backend ไม่ใช่ sample standard deviation

## 5. ลำดับรับผิดชอบทั้ง 4 คน (เปลี่ยนผู้รับผิดชอบได้ แต่คงลำดับ)

เวลาเป้าหมายรวม 9:40 นาที ทุกคนแนะนำตอนเรียน รหัส ชื่อ-สกุล และเห็นหน้าขณะนำเสนอ
ตอนเรียนให้ใส่ค่าจริง เพราะ README โปรเจกต์ไม่ได้ระบุไว้

### เปิดคลิป 0:00–0:40 — ทุกคน

ชื่อโครงงาน ระบบประกาศคะแนนสอบ กลุ่ม G12 แล้วแนะนำตัวคนละประมาณ 8 วินาที

### คนที่ 1: ชฎาภา อนุกูลเรืองรุ่ง — 670510698 (0:40–2:30)

หน้าจอ: Sign up → Login → Teacher Courses

1. สมัคร ธนกฤต วงศ์สุวรรณ ด้วยข้อมูลบัญชีด้านบน
   - คาดหวัง: สมัครสำเร็จ เกิดแถว auth_users และ students ที่เชื่อมกัน
   - Capture A01: ฟอร์ม/ผลสำเร็จ + SQL จริง + ผล SQL หัวข้อ 11 ส่วน A (ไม่แสดง password hash)
2. Login อาจารย์ด้วย kittipong.wat@cmu.ac.th / GradeBook69!
   - คาดหวัง: เข้าหน้า Teacher Courses
   - Capture A02: หน้า login/ผลปลายทาง + SQL lookup ผู้ใช้จริงที่ใช้ตรวจบัญชี
3. สร้าง 204321 / Database System / Section 001
   - คาดหวัง: มีแถว courses ใหม่ join_open = true, is_deleted = false, is_archive = false
   - Capture A03: ฟอร์ม/การ์ดวิชา + SQL จริง + SQL หัวข้อ 11 ส่วน B
4. แก้ชื่อวิชาเป็น Database Systems โดยคง Course ID 204321
   - Capture A04: ชื่อก่อน–หลังบน UI และแถว courses หลังเปลี่ยน
5. ส่ง course_code และ join_code จริงให้คนที่ 2

คำพูดหลัก: “ระบบแยกบัญชีอาจารย์กับนักศึกษา และอาจารย์สร้างวิชาพร้อมรหัสเข้าร่วมให้ผู้เรียน”

### คนที่ 2: ฐิติพันธ์ วงศ์สุรดาพร — 670510703 (2:30–4:15)

หน้าจอ: Student Dashboard + Join dialog → Student Course Detail

1. Login ธนกฤต วงศ์สุวรรณ แล้วเปิด Dashboard ก่อนเข้าร่วม
   - ถ้าบัญชีใหม่จริง คาดหวัง: ยังไม่มีวิชา 204321
2. กรอก join_code ที่คนที่ 1 ส่งให้ ตรวจชื่อวิชาและ Section 001 แล้วกดยืนยัน
   - คาดหวัง: enrollments ของ 690510903 มี status = active, joined_via = code
   - enrollment.section ตอน join อาจเป็น NULL; UI แสดง 001 จากค่า courses.section
   - Capture B01: join preview/ผลบน Dashboard + SQL จริง + SQL หัวข้อ 11 ส่วน C
3. เปิด Course Detail ก่อนมีคะแนนประกาศ
   - คาดหวัง: เห็นวิชาและอาจารย์ แต่ assessments ว่าง Weighted Average = 0
   - Capture B02: UI ที่ไม่มีคะแนน + SQL SELECT จริง
4. ส่งต่อสถานะ “นักศึกษา 3 เข้าร่วมแล้ว ยังไม่มีคะแนน” ให้คนที่ 3

คำพูดหลัก: “ข้อมูลการเข้าร่วมถูกเก็บแยกจากคะแนน นักศึกษาจึงเห็นรายวิชาได้แม้ยังไม่ถูกให้คะแนน”

### คนที่ 3: นภิสา ศรีทุมมา — 670510711 (4:15–6:50)

หน้าจอ: Teacher Assignment Management → Teacher Grade

1. Login อาจารย์ เปิดวิชาเดียวกัน สร้าง Midterm / Full Mark 100 / Weight 100
   - คาดหวัง: quizzes มี Midterm, is_publish = false
   - Capture C01: งานใหม่ + SQL จริง + SQL หัวข้อ 11 ส่วน D
2. เปิด Grade ของ Midterm อัปโหลด midterm_scores.csv
   - คาดหวัง: 5 คน คะแนน 60,70,80,90,100; unread_flag ทุกคน = true
   - enrollments รวม 5 active: ธนกฤต วงศ์สุวรรณ joined_via = code; อีก 4 คน joined_via = csv
   - enrollment.section ทุกคน = 001; uploads มีชื่อไฟล์ที่นำเข้า
   - Capture C02: ผลนำเข้า/UI คะแนน + SQL จริง + SQL หัวข้อ 11 ส่วน C/E/F
3. Publish Midterm ครั้งแรก
   - คาดหวัง: quizzes.is_publish = true
   - Capture C03: UI หลังประกาศ + SQL UPDATE จริง + SQL หัวข้อ 11 ส่วน D
4. อัปโหลด midterm_scores_revised.csv ที่งาน Midterm เดิม
   - คาดหวัง: ธนกฤต วงศ์สุวรรณ = 85; score_id เดิม; จำนวนคะแนนยัง 5; is_publish กลับเป็น false
   - ทุกแถวที่ matched ถูกตั้ง unread_flag = true อีกครั้ง แม้ตัวเลขคะแนนบางคนไม่เปลี่ยน
   - Capture C04: คะแนน 80→85 + จำนวนแถว/score_id ก่อน–หลัง + is_publish = false
5. กด Publish อีกครั้งก่อนส่งต่อคนที่ 4
   - Capture C05: is_publish = true + SQL หัวข้อ 11 ส่วน G (สถิติหลังแก้)

คำพูดหลัก: “อัปโหลดซ้ำแก้คะแนนเดิม และระบบยกเลิกสถานะประกาศเพื่อให้อาจารย์ตรวจแล้วประกาศใหม่”

### คนที่ 4: ศุภาการ แก้วพวงใหม่ — 670510728 (6:50–9:20)

หน้าจอ: Student Course Detail → Student Score → Teacher Assignment/Grade

1. Login ธนกฤต วงศ์สุวรรณ เปิด Course Detail ใหม่
   - คาดหวัง: เห็น Midterm; Weighted Average 85.00; unread_flag ก่อนเปิด Score = true
   - Capture D01: UI และผล SELECT จริง
2. เปิด Score ของ Midterm
   - คาดหวัง: 85/100, 85%, Rank 3/5, Mean 81, Median 85, Std 14.28, High 100, Low 60
   - เกิด UPDATE unread_flag ของ ธนกฤต วงศ์สุวรรณ เป็น false; ของอีก 4 คนยัง true
   - Capture D02: UI คะแนน/สถิติ + SQL จริง + SQL หัวข้อ 11 ส่วน E/G
3. สลับ browser อาจารย์ สร้าง แบบฝึกหัด ER Diagram / Full Mark 20 / Weight 10 แล้วนำเข้า er_diagram_scores.csv
   - คาดหวัง: มีคะแนน ธนกฤต วงศ์สุวรรณ = 15 และงานนี้ไม่ Publish
4. ลบคะแนน ธนกฤต วงศ์สุวรรณ จาก แบบฝึกหัด ER Diagram
   - คาดหวัง: scores.is_deleted = true; Query รายการคะแนน active ไม่พบแถวนั้น
   - Capture D03: UI ก่อน–หลัง + SQL UPDATE จริง + SQL หัวข้อ 11 ส่วน H
5. ลบงาน แบบฝึกหัด ER Diagram
   - คาดหวัง: quizzes.is_deleted = true; ไม่ปรากฏในรายการงาน active; Midterm ยังอยู่
   - Capture D04: UI ก่อน–หลัง + SQL UPDATE จริง + SQL หัวข้อ 11 ส่วน H

คำพูดหลัก: “นักศึกษาดูคะแนนตนเองพร้อมสถิติ และเมื่อเปิดอ่าน ระบบบันทึกสถานะให้อาจารย์เห็น การลบเป็น Soft delete”

### ปิดคลิป 9:20–9:40 — คนที่ 4

สรุปว่าระบบจัดการวิชา รับคะแนนจาก CSV ประกาศคะแนน และให้นักศึกษาดูผลได้

## 6. ตารางรับช่วง (เติมค่าจริงร่วมกัน)

| ค่า | ค่าจริงจากการรัน |
|---|---|
| URL frontend / backend ที่ทุกคนใช้ | ... |
| ฐานข้อมูลทดสอบ | ... |
| teacher_id ของ kittipong.wat | ... |
| course_code ของ 204321 | ... |
| join_code ของ 204321 | ... |
| quiz_id ของ Midterm | ... |
| score_id ของ ธนกฤต วงศ์สุวรรณ ใน Midterm ก่อนแก้ | ... |
| score_id ของ ธนกฤต วงศ์สุวรรณ ใน Midterm หลังแก้ (ต้องเท่ากัน) | ... |
| quiz_id ของ แบบฝึกหัด ER Diagram | ... |
| ตอนเรียนจริงของสมาชิกแต่ละคน | ... |

## 7. เคสเสริมสำหรับซ้อม/ตอบคำถาม (ทำหลังอัดเส้นหลัก)

ใช้ Midterm ที่ยังไม่ Publish หรือสร้างงาน “แบบฝึกหัด SQL” แยก เพราะการนำเข้า CSV ที่ parse ผ่านจะบันทึก uploads และอาจเปลี่ยน is_publish แม้ matched = 0

| เคส | ข้อมูล/การกระทำ | ผลที่คาดหวังตามโค้ด |
|---|---|---|
| รหัสผ่านผิด | thanakrit_wong@cmu.ac.th / WrongPassword1! | Login ไม่สำเร็จ HTTP 401 |
| สมัคร email ซ้ำ | ข้อมูล ธนกฤต วงศ์สุวรรณ เดิม | ไม่สร้างบัญชีเพิ่ม HTTP 409 |
| Student ID ซ้ำกับ email ใหม่ | 690510903 / thanakrit_new@cmu.ac.th | HTTP 409 ไม่เพิ่ม students |
| ขาดหัว section | error_missing_column.csv | HTTP 400 missing columns section; ไม่บันทึก upload |
| คะแนนไม่ใช่ตัวเลข | error_invalid_score.csv | HTTP 400 invalid score on line 2; ไม่บันทึก upload |
| Email ไม่ตรง ID | error_email_mismatch.csv | matched = 0, unmatched มี reason email_mismatch; คะแนนไม่เปลี่ยน |
| ยังไม่สมัคร | error_not_registered.csv | matched = 0, unmatched มี reason not_registered; ไม่สร้างบัญชี/คะแนน |
| ปิดรับเข้าร่วม | ปิด join_open แล้วลอง join ด้วยนักศึกษาที่ยังไม่เข้าวิชา | เข้าร่วมไม่ได้ เปิดรับคืนเมื่อทดสอบเสร็จ |
| ออกรายวิชาโดยอาจารย์ | Remove ปวริศ สุขเกษม | enrollment.status = dropped; กลับเข้าร่วมได้เมื่อเปิดรับ |
| Archive/Restore | Archive 204321 แล้ว Restore | is_archive true→false; กลับมาใน Dashboard อาจารย์ |
| ลบวิชา | สร้างวิชา 204321-LAB แล้วลบ | is_deleted = true; ไม่ลบ 204321 หลัก |

ไม่กำหนดเคส “คะแนนติดลบ/เกินเต็มต้องถูกปฏิเสธ” ว่าผ่านแน่นอน เพราะโค้ด CSV ปัจจุบันยังไม่ได้ตรวจช่วงคะแนน
การไม่เห็นงานยังไม่ Publish บนหน้า Course Detail เป็นพฤติกรรมหน้า UI; เอกสารนี้ไม่ได้รับรองการป้องกันเข้าถึงผ่าน URL โดยตรง

## 8. SQL และหลักฐานที่ต้องเตรียม

คัดลอก SQL ในหัวข้อ 11 ไปเปิดใน pgAdmin Query Tool และรันแต่ละส่วน ณ จังหวะที่เอกสารระบุ แสดงชื่อคอลัมน์และ record ที่ตรวจ
ส่วน SQL ที่ระบบใช้ให้เก็บจาก log/SQL trace ระหว่างกด UI จริง พร้อม parameters ที่เป็นข้อมูลสมมติ
SQLAlchemy จะส่งหลายคำสั่ง โดยเฉพาะสมัครสมาชิกและ CSV อย่าอ้างว่าตัวอย่าง SQL ด้านล่างเป็น trace จริงครบทุกคำสั่ง

ตัวอย่าง SQL เทียบเท่าสำหรับอธิบาย (แทน :... ด้วยค่าจริงเฉพาะถ้าต้องใช้; ไม่ต้องรันซ้ำเพื่อเดโม):

```sql
-- แก้ชื่อวิชา
UPDATE courses SET course_name = 'Database Systems'
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
- ถ้าทำซ้ำในฐานเดิม อย่าสมัครบัญชีหรือสร้าง 204321/Midterm ซ้ำ; ข้ามส่วนที่มีแล้วหรือใช้ฐานทดสอบแยกรอบ
- อัปโหลด midterm_scores.csv ซ้ำช่วยคืนคะแนน แต่ไม่คืนสถานะ enrollment/บัญชี/วิชาให้เหมือนเริ่มต้นทั้งหมด
- ถ้าต้องการคืน unread_flag เป็น true สำหรับซ้อมหน้า Score ให้อัปโหลดไฟล์คะแนนอีกครั้งและ Publish ใหม่
- ทดสอบเคสเสริมหลังเก็บวิดีโอเส้นหลักเพื่อไม่ให้จำนวนผู้เรียนและสถิติผิดจากตาราง
- ก่อนส่งตรวจวิดีโอไม่เกิน 10 นาที เห็นหน้าผู้นำเสนอทั้ง 4 คน และมีตัวอย่างทุกหน้าจอในขอบเขตงาน

## 10. เนื้อหา CSV ทุกชุด — คัดลอกจากไฟล์นี้ได้เลย

คัดลอกเฉพาะข้อความในกรอบ csv ของแต่ละชุดไปบันทึกตามชื่อที่กำหนด ใช้ UTF-8 และนามสกุล .csv
ไฟล์นี้มีข้อมูลครบในตัว ไม่จำเป็นต้องเปิดชุดไฟล์เดิมใน design/demo
CSV ข้อมูลคะแนนมีหัว student_email; CSV บัญชีมีหัว email ทั้งสองประเภทใช้คนละหน้าที่

### 10.1 บัญชีสำหรับกรอกสมัครสมาชิก (accounts.csv)

```csv
role,student_id,first_name,last_name,email,password
teacher,,กิตติพงศ์,วัฒนกุล,kittipong.wat@cmu.ac.th,GradeBook69!
student,690510901,ณัฐวุฒิ,ศรีสุข,nattawut_sri@cmu.ac.th,GradeBook69!
student,690510902,พิมพ์ชนก,ใจดี,pimchanok_jai@cmu.ac.th,GradeBook69!
student,690510903,ธนกฤต,วงศ์สุวรรณ,thanakrit_wong@cmu.ac.th,GradeBook69!
student,690510904,ชนัญชิดา,อินทร์แก้ว,chananchida_in@cmu.ac.th,GradeBook69!
student,690510905,ปวริศ,สุขเกษม,pawarit_suk@cmu.ac.th,GradeBook69!
```

### 10.2 คะแนน Midterm ครั้งแรก — matched 5 (midterm_scores.csv)

```csv
student_id,student_email,score,section,name
690510901,nattawut_sri@cmu.ac.th,60,001,ณัฐวุฒิ ศรีสุข
690510902,pimchanok_jai@cmu.ac.th,70,001,พิมพ์ชนก ใจดี
690510903,thanakrit_wong@cmu.ac.th,80,001,ธนกฤต วงศ์สุวรรณ
690510904,chananchida_in@cmu.ac.th,90,001,ชนัญชิดา อินทร์แก้ว
690510905,pawarit_suk@cmu.ac.th,100,001,ปวริศ สุขเกษม
```

### 10.3 คะแนน Midterm หลังแก้ไข — matched 5 และคะแนนรวมยัง 5 แถว (midterm_scores_revised.csv)

```csv
student_id,student_email,score,section,name
690510901,nattawut_sri@cmu.ac.th,60,001,ณัฐวุฒิ ศรีสุข
690510902,pimchanok_jai@cmu.ac.th,70,001,พิมพ์ชนก ใจดี
690510903,thanakrit_wong@cmu.ac.th,85,001,ธนกฤต วงศ์สุวรรณ
690510904,chananchida_in@cmu.ac.th,90,001,ชนัญชิดา อินทร์แก้ว
690510905,pawarit_suk@cmu.ac.th,100,001,ปวริศ สุขเกษม
```

### 10.4 คะแนนแบบฝึกหัด ER Diagram — matched 1 (er_diagram_scores.csv)

```csv
student_id,student_email,score,section,name
690510903,thanakrit_wong@cmu.ac.th,15,001,ธนกฤต วงศ์สุวรรณ
```

### 10.5 อีเมลไม่ตรงกับรหัสนักศึกษา — matched 0 / email_mismatch (error_email_mismatch.csv)

```csv
student_id,student_email,score,section,name
690510903,thanakrit_wrong@cmu.ac.th,85,001,ธนกฤต วงศ์สุวรรณ
```

### 10.6 นักศึกษายังไม่สมัคร — matched 0 / not_registered (error_not_registered.csv)

```csv
student_id,student_email,score,section,name
690510999,anawat_porn@cmu.ac.th,75,001,อนาวัฒน์ พรชัย
```

### 10.7 คะแนนเป็นข้อความ — HTTP 400 (error_invalid_score.csv)

```csv
student_id,student_email,score,section,name
690510903,thanakrit_wong@cmu.ac.th,abc,001,ธนกฤต วงศ์สุวรรณ
```

### 10.8 ขาดหัวคอลัมน์ section — HTTP 400 (error_missing_column.csv)

```csv
student_id,student_email,score
690510903,thanakrit_wong@cmu.ac.th,85
```

## 11. SQL ตรวจฐานข้อมูลจริง — คัดลอกไปใช้ใน pgAdmin

คำสั่งต่อไปนี้เป็น SELECT สำหรับตรวจหลักฐาน ไม่มีคำสั่งแก้ไขข้อมูล รันเฉพาะส่วนที่ตรงกับช่วงนำเสนอ
A = บัญชี, B = วิชา, C = การเข้าร่วม, D = งาน/การประกาศ, E = คะแนน/สถานะอ่าน, F = ประวัติ CSV,
G/G2/G3 = สถิติ/อันดับ/คะแนนถ่วงน้ำหนัก, H1/H2/H3 = หลักฐานการลบ
หาก B ได้มากกว่าหนึ่งวิชาจากบัญชีอาจารย์เดียวกัน ให้เลือก course_code ของรอบที่นำเสนอและเพิ่มเงื่อนไขใน selected_course ก่อนใช้ผลรวม

```sql
-- Read-only PostgreSQL verification. Run each section at its matching presentation step.
-- If section B returns more than one course, resolve the selected course selection before continuing.


-- A: accounts; expected teacher + 5 students after live signup (no password column).
SELECT a.email, s.student_id,
       COALESCE(s.first_name, t.first_name) AS first_name,
       COALESCE(s.last_name, t.last_name) AS last_name,
       CASE WHEN s.student_id IS NOT NULL THEN 'student' ELSE 'teacher' END AS role
FROM auth_users a LEFT JOIN students s ON s.auth_user_id = a.auth_user_id
LEFT JOIN teachers t ON t.auth_user_id = a.auth_user_id
WHERE a.email IN ('kittipong.wat@cmu.ac.th', 'nattawut_sri@cmu.ac.th',
 'pimchanok_jai@cmu.ac.th', 'thanakrit_wong@cmu.ac.th', 'chananchida_in@cmu.ac.th', 'pawarit_suk@cmu.ac.th')
ORDER BY a.email;


WITH selected_course AS (
    SELECT c.course_code FROM courses c
    JOIN teachers t ON t.teacher_id = c.teacher_id
    JOIN auth_users a ON a.auth_user_id = t.auth_user_id
    WHERE c.course_id = '204321' AND a.email = 'kittipong.wat@cmu.ac.th'
)
-- B: expected one selected course; capture course_code and generated join_code.
SELECT c.course_code, c.course_id, c.course_name, c.section, c.teacher_id,
       c.join_code, c.join_open, c.is_archive, c.is_deleted
FROM courses c JOIN selected_course d ON d.course_code = c.course_code;


WITH selected_course AS (
    SELECT c.course_code FROM courses c
    JOIN teachers t ON t.teacher_id = c.teacher_id
    JOIN auth_users a ON a.auth_user_id = t.auth_user_id
    WHERE c.course_id = '204321' AND a.email = 'kittipong.wat@cmu.ac.th'
)
-- C: expected 1 enrollment after join; 5 after CSV import.
SELECT e.enrollment_id, e.student_id, e.course_code, e.section,
       COALESCE(e.section, c.section) AS displayed_section, e.status, e.joined_via
FROM enrollments e JOIN selected_course d ON d.course_code = e.course_code
JOIN courses c ON c.course_code = e.course_code
ORDER BY e.student_id;


WITH selected_course AS (
    SELECT c.course_code FROM courses c
    JOIN teachers t ON t.teacher_id = c.teacher_id
    JOIN auth_users a ON a.auth_user_id = t.auth_user_id
    WHERE c.course_id = '204321' AND a.email = 'kittipong.wat@cmu.ac.th'
)
-- D: quiz IDs and publication/deletion state.
SELECT q.quiz_id, q.quiz_name, q.full_mark, q.weight, q.is_publish, q.is_deleted
FROM quizzes q JOIN selected_course d ON d.course_code = q.course_code
ORDER BY q.quiz_name, q.quiz_id;


WITH selected_course AS (
    SELECT c.course_code FROM courses c
    JOIN teachers t ON t.teacher_id = c.teacher_id
    JOIN auth_users a ON a.auth_user_id = t.auth_user_id
    WHERE c.course_id = '204321' AND a.email = 'kittipong.wat@cmu.ac.th'
)
-- E: main scores and read state. Record score_id before and after reimport.
SELECT s.score_id, s.student_id, a.email, s.score, s.unread_flag,
       s.is_deleted, s.updated_at, q.quiz_id
FROM scores s JOIN quizzes q ON q.quiz_id = s.quiz_id
JOIN selected_course d ON d.course_code = q.course_code
JOIN students st ON st.student_id = s.student_id
JOIN auth_users a ON a.auth_user_id = st.auth_user_id
WHERE q.quiz_name = 'Midterm' AND q.is_deleted = false
ORDER BY s.student_id;


WITH selected_course AS (
    SELECT c.course_code FROM courses c
    JOIN teachers t ON t.teacher_id = c.teacher_id
    JOIN auth_users a ON a.auth_user_id = t.auth_user_id
    WHERE c.course_id = '204321' AND a.email = 'kittipong.wat@cmu.ac.th'
)
-- F: import log. uploads does not store quiz_id in the current model.
SELECT u.upload_id, u.file_name, u.course_code, u.created_at
FROM uploads u JOIN selected_course d ON d.course_code = u.course_code
ORDER BY u.created_at, u.upload_id;


WITH selected_course AS (
    SELECT c.course_code FROM courses c
    JOIN teachers t ON t.teacher_id = c.teacher_id
    JOIN auth_users a ON a.auth_user_id = t.auth_user_id
    WHERE c.course_id = '204321' AND a.email = 'kittipong.wat@cmu.ac.th'
)
, main_scores AS (
 SELECT s.quiz_id, s.student_id, s.score FROM scores s
 JOIN quizzes q ON q.quiz_id = s.quiz_id
 JOIN selected_course d ON d.course_code = q.course_code
 WHERE q.quiz_name = 'Midterm' AND q.is_deleted = false AND s.is_deleted = false
)
-- G: population std matches backend. Expected after update: 5,81,85,14.28,100,60.
SELECT quiz_id, COUNT(*) AS total_students,
 ROUND(AVG(score)::numeric, 2) AS mean,
 ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY score))::numeric, 2) AS median,
 ROUND(STDDEV_POP(score)::numeric, 2) AS std,
 MAX(score) AS highest, MIN(score) AS lowest
FROM main_scores GROUP BY quiz_id;


WITH selected_course AS (
    SELECT c.course_code FROM courses c
    JOIN teachers t ON t.teacher_id = c.teacher_id
    JOIN auth_users a ON a.auth_user_id = t.auth_user_id
    WHERE c.course_id = '204321' AND a.email = 'kittipong.wat@cmu.ac.th'
)
-- G2: percent/rank for ธนกฤต วงศ์สุวรรณ; expected 85%, rank 3.
SELECT s.student_id, s.score, q.full_mark,
 ROUND((s.score / NULLIF(q.full_mark, 0) * 100)::numeric, 2) AS percent,
 1 + (SELECT COUNT(*) FROM scores higher
      WHERE higher.quiz_id = s.quiz_id AND higher.is_deleted = false
        AND higher.score > s.score) AS ranking
FROM scores s JOIN quizzes q ON q.quiz_id = s.quiz_id
JOIN selected_course d ON d.course_code = q.course_code
WHERE q.quiz_name = 'Midterm' AND q.is_deleted = false
 AND s.student_id = '690510903' AND s.is_deleted = false;


WITH selected_course AS (
    SELECT c.course_code FROM courses c
    JOIN teachers t ON t.teacher_id = c.teacher_id
    JOIN auth_users a ON a.auth_user_id = t.auth_user_id
    WHERE c.course_id = '204321' AND a.email = 'kittipong.wat@cmu.ac.th'
)
-- G3: published weighted average; expected 85.00 with only Midterm published.
SELECT q.course_code,
 ROUND((100.0 * SUM(CASE WHEN s.score IS NOT NULL AND q.full_mark > 0
       THEN s.score / q.full_mark * q.weight ELSE 0 END)
       / NULLIF(SUM(q.weight), 0))::numeric, 2) AS weighted_average
FROM quizzes q JOIN selected_course d ON d.course_code = q.course_code
LEFT JOIN scores s ON s.quiz_id = q.quiz_id AND s.student_id = '690510903'
 AND s.is_deleted = false
WHERE q.is_deleted = false AND q.is_publish = true
GROUP BY q.course_code;


WITH selected_course AS (
    SELECT c.course_code FROM courses c
    JOIN teachers t ON t.teacher_id = c.teacher_id
    JOIN auth_users a ON a.auth_user_id = t.auth_user_id
    WHERE c.course_id = '204321' AND a.email = 'kittipong.wat@cmu.ac.th'
)
-- H1: physical rows retained after soft delete (expect is_deleted=true).
SELECT q.quiz_id, q.quiz_name, q.is_deleted AS quiz_deleted,
       s.score_id, s.student_id, s.score, s.is_deleted AS score_deleted
FROM quizzes q JOIN selected_course d ON d.course_code = q.course_code
LEFT JOIN scores s ON s.quiz_id = q.quiz_id
WHERE q.quiz_name = 'แบบฝึกหัด ER Diagram';


WITH selected_course AS (
    SELECT c.course_code FROM courses c
    JOIN teachers t ON t.teacher_id = c.teacher_id
    JOIN auth_users a ON a.auth_user_id = t.auth_user_id
    WHERE c.course_id = '204321' AND a.email = 'kittipong.wat@cmu.ac.th'
)
-- H2: after score deletion, expected no active practice score.
SELECT s.score_id, s.student_id, s.score
FROM scores s JOIN quizzes q ON q.quiz_id = s.quiz_id
JOIN selected_course d ON d.course_code = q.course_code
WHERE q.quiz_name = 'แบบฝึกหัด ER Diagram' AND s.is_deleted = false;


WITH selected_course AS (
    SELECT c.course_code FROM courses c
    JOIN teachers t ON t.teacher_id = c.teacher_id
    JOIN auth_users a ON a.auth_user_id = t.auth_user_id
    WHERE c.course_id = '204321' AND a.email = 'kittipong.wat@cmu.ac.th'
)
-- H3: after assignment deletion, expected no active practice assignment.
SELECT q.quiz_id, q.quiz_name FROM quizzes q
JOIN selected_course d ON d.course_code = q.course_code
WHERE q.quiz_name = 'แบบฝึกหัด ER Diagram' AND q.is_deleted = false;
```

## 12. ภาพรวมฐานข้อมูลที่ควรเห็นเมื่อจบเส้นหลัก

| ตาราง | สถานะเฉพาะข้อมูลชุดนี้ |
|---|---|
| auth_users | 6 บัญชี: อาจารย์ 1 + นักศึกษา 5 |
| teachers | อาจารย์กิตติพงศ์ 1 คน |
| students | นักศึกษา 5 คน ตามรหัสและอีเมลในหัวข้อ 2 |
| courses | 204321 ชื่อ Database Systems ตอนเรียน 001 ไม่ archive และไม่ delete |
| enrollments | 5 active; ธนกฤตเข้าทาง code อีก 4 คนทาง csv; section ทุกคน 001 หลังนำเข้า |
| quizzes | Midterm: is_publish=true, is_deleted=false; แบบฝึกหัด ER Diagram: is_publish=false, is_deleted=true |
| scores | Midterm 5 แถว active: 60,70,85,90,100; แบบฝึกหัด 1 แถวคะแนน 15 ที่ is_deleted=true |
| unread_flag ของ Midterm | ธนกฤต false หลังเปิด Score; อีก 4 คน true หากยังไม่ได้เปิด |
| uploads | 3 รายการ: midterm_scores.csv, midterm_scores_revised.csv, er_diagram_scores.csv |

จำนวนข้างต้นนับเฉพาะรอบหลักที่ทำครั้งเดียว ไม่รวมเคสเสริมและข้อมูลเดิมในฐานข้อมูล

รายการสุดท้ายก่อนอัด: ใส่ตอนเรียนสมาชิกจริง → สมัครบัญชีที่ระบุให้เตรียมล่วงหน้า → ใช้ backend/database เดียวกัน → จดค่าที่ระบบสร้าง → เดินตามคนที่ 1 ถึง 4 → เก็บภาพ UI, SQL จริง และผล PostgreSQL → ตรวจความยาวไม่เกิน 10 นาที
