# UI ↔ Database Review (schema v1)

Audit of every screen in `design/ui/` and the implemented Vue components against the
current schema (`fastapi/app/models/`, `design/database/database_schema.png`).

Legend — **OK** = fully backed by the DB · **Partial** = renderable but only through a
workaround or wrong data · **Missing** = no DB support at all.

---

## 1. Screen-by-screen mapping

### `v1/login.png`, `v1/sign_up.png` — Auth

| UI element | Backed by | Verdict |
|---|---|---|
| Email + password | `auth_users.email`, `auth_users.password` | OK |
| First / Middle / Last name | `students.*` or `teachers.*` | Partial — duplicated in two tables |
| "ID" field (student no.) | `students.student_id` (PK) | Partial |
| Sign up / in with Google | `auth_providers` | Partial — no uniqueness guarantee |
| Role (student vs teacher) | *derived* | **Missing** |

Findings:

- **Role is not stored.** `auth.py` decides with `"student" if user.student else "teacher"`
  (`fastapi/app/routers/auth.py:224`, `:346`). Any auth user with neither profile is
  silently treated as a teacher, and `/me` then raises `AttributeError` on
  `current_user.teacher.first_name`.
- **Role is inferred from the signup form.** `register()` branches on whether
  `student_id` was submitted (`auth.py:257`). A teacher who types anything into the ID
  box is registered down the student path.
- **`password IS NULL` is an implicit account state.** It is the sentinel for
  "invited by CSV, not yet registered" (`auth.py:270`). Nothing names or constrains it.
- `auth_providers` has **no `UNIQUE (provider, provider_user_id)`**, yet `google_auth()`
  looks the row up with `.first()` and assumes it is unique (`auth.py:148`).
- `students.auth_user_id` / `teachers.auth_user_id` have **no unique constraint**, so the
  DB permits many student rows per login even though the ORM declares `uselist=False`.

### `v1/teacher_edit_courses.png`, `v0/teacher_courses.png`, `v1/popup_create.png` — Course Management

| UI element | Backed by | Verdict |
|---|---|---|
| Course code `CS101` | `courses.course_id` | Partial — misnamed |
| Course title | `courses.course_name` | OK |
| "142 STUDENTS" enrolled | *counted from `scores`* | **Partial / wrong** |
| Section label | `scores.section` | **Partial / wrong** |
| "Current Semester: Fall 2023" + term dropdown | — | **Missing** |
| Schedule "Mon/Wed 10:00–11:30" | — | **Missing** |
| Status chip: In Progress / Published | — | **Missing** |
| Stat tiles: Total Students / Pending Grades / Published Courses | — | **Missing** |
| Search, pagination | any | OK (client-side) |
| Archive / delete | `is_archive`, `is_deleted` | OK |

Findings:

- **The enrolled count is not an enrolled count.** `teacher_dashboard()` walks every quiz
  and every score in the course and counts distinct `student_id`
  (`fastapi/app/routers/teacher.py:29-37`). It reports *students who already have at least
  one score*, so a freshly created course shows 0 students, and rendering one number costs
  a full scan of the course's scores.
- **The section shown on the card is arbitrary.** The same function takes
  `.first()` score row in the whole course and displays its `section`
  (`teacher.py:39-43`). With two sections, which one appears is undefined.
- **Column naming is inverted.** `courses.course_code` is the surrogate integer PK;
  `courses.course_id` is the human code (`CS101`) that the UI labels "Course Code".
  `course_id` has no unique constraint.
- **No term/semester entity**, so `CS101` taught in Fall 2023 and Spring 2024 must be two
  unrelated `courses` rows, and the term filter in the mockup cannot be built.
- The create-course dialog only collects a name, but the API also requires `course_id`
  and the UI needs a section and a term.

### `v1/teacher_edit_assignments.png` — Assignments

| UI element | Backed by | Verdict |
|---|---|---|
| Assignment name | `quizzes.quiz_name` | OK |
| Full mark, weight | `quizzes.full_mark`, `quizzes.weight` | OK |
| Delete assignment | `quizzes.is_deleted` | OK |
| Assignment type (Exam / Quiz / Project) | — | **Missing** |
| Subtitle / description | — | **Missing** |
| Due date | — | **Missing** |
| Ordering in the list | — | **Missing** |

Findings:

- **Entity name mismatch.** The table is `quizzes`; every screen calls them Assignments or
  Assessments. The API already translates on the way out (`quiz_id` → `assign_id`,
  `quiz_name` → `assign_name`, `teacher.py:80-86`), which is a symptom, not a fix.
- `v0/GPA.png` and `v1/stu_assignments.png` show a **description line** under each title
  ("In-class written exam", "Algorithm Implementation") and a **DUE DATE** column. Neither
  column exists.
- **Weights are unconstrained.** Nothing checks that a course's weights sum to 100, and
  `weight` is a plain float with no `CHECK (weight >= 0)`.

### `v1/teacher_edit_score.png`, `v0/edit_grade.png` — Grade sheet

| UI element | Backed by | Verdict |
|---|---|---|
| Student avatar / name / ID | `students.*` | OK |
| Score input | `scores.score` | OK |
| "Section A" chip | `scores.section` | Partial — see above |
| Status Read / Unread | `scores.unread_flag` | Partial |
| Status **Pending** (`--`, no score yet) | — | **Missing** |
| "LAST UPDATED Oct 24, 10:42 AM" | `scores.updated_at` | OK |
| Who changed the grade / previous value | — | **Missing** |
| Import CSV | `uploads` | Partial |
| Publish Scores | `quizzes.is_publish` | Partial |
| Filter counts (Read 12 / Unread 4) | derived | Partial |
| Showing 1–5 of 34 students | — | **Missing** |

Findings:

- **A student with no score cannot appear on this screen.** The roster *is* the score
  table (`teacher.py:105`), so the "Pending / `--`" row the mockup shows for Charlie Brown
  is unrepresentable: no score row means the student is invisible, and "34 students" cannot
  be counted.
- **`uploads` does not record what it uploaded.** `upload_csv()` receives `quiz_id` in the
  path but stores only `file_name`, `teacher_id`, `course_code` (`teacher.py:196-204`).
  There is no link to the assignment, no row/error counts, no status, no stored file — so
  no import history, no re-import, no rollback.
- **Publish state is a bare boolean.** No `published_at`, no publisher, so
  "Last synced today at 9:41 AM" and any publish history are not expressible. Re-uploading
  silently flips `is_publish` back to false (`teacher.py:194`) with no record of it.
- **`unread_flag` is a boolean, not a receipt.** No read timestamp, so "Read" cannot be
  ordered or audited.

### `v1/stu_course.png`, `v0/subject.png` — Student dashboard

| UI element | Backed by | Verdict |
|---|---|---|
| "Hello, Alex" + student ID | `students.*` | OK |
| Enrolled course list | *derived from `scores`* | **Partial / wrong** |
| "Current Enrolled Courses 5" | — | **Missing** |
| Course code + title | `courses.*` | OK |
| "Spring 2024 • Prof. Alan Turing" | `teachers.*`; term **Missing** | Partial |
| "NEW GRADE" badge | derived from `unread_flag` | Partial |
| Sort by recent | — | **Missing** |

Findings:

- **A student sees only courses in which they already have a score**
  (`fastapi/app/routers/student.py:26-42`). Enroll a student today, and their dashboard is
  empty until a grade is uploaded. The "5 enrolled courses" count is really "5 courses with
  grades".
- That loop also filters `course.is_deleted` but **not** `Score.is_deleted` or
  `Quiz.is_deleted`, so soft-deleted grades still resurrect a course card.
- The "NEW GRADE" badge would require scanning every score of every quiz of the course; the
  dashboard endpoint does not compute it at all today.

### `v1/stu_assignments.png` — Course detail

| UI element | Backed by | Verdict |
|---|---|---|
| Course code + title | `courses.*` | OK |
| "ACTIVE" chip, "Fall 2023" | — | **Missing** |
| Instructor name | `teachers.*` | OK |
| **Contact** button | `auth_users.email` | Partial — no reachable contact record |
| Assessment title | `quizzes.quiz_name` | OK |
| Assessment description | — | **Missing** |
| Weight % | `quizzes.weight` | OK |
| Read / Unread status | `scores.unread_flag` | OK |
| Weighted Average 92.00 | computed in Python | OK |

Findings:

- Enrollment is again checked by "does a score row exist" (`student.py:73`), which returns
  **403 Not enrolled** to a genuinely enrolled student who has not been graded yet.
- `student_course_detail()` reaches `course.teacher.first_name` with no null guard
  (`student.py:120`); `courses.teacher_id` is `nullable=False`, so this holds today, but
  the model has no path for a course with no instructor or with two.

### `v1/stu_score.png`, `v0/GPA.png` — Score detail & statistics

| UI element | Backed by | Verdict |
|---|---|---|
| My score / full mark / % | `scores.score`, `quizzes.full_mark` | OK |
| "Graded" chip | derived | Partial |
| Mean / median / std / high / low | computed per request | **Partial** |
| Total participants | computed per request | Partial |
| Score distribution + "YOU" marker | computed per request | Partial |
| Grade letter "GRADE A", final GPA | — | **Missing** |
| "Top 5% of class" | rank computed per request | Partial |
| Download Report | — | **Missing** |

Findings:

- `student_score_detail()` **loads every score row of the assessment on every page view**
  and computes mean/median/σ/rank in Python (`student.py:150-209`). Correct at 34 students,
  linear in class size, and repeated for every student who opens the page.
- No grading scale exists, so "GRADE A" and the GPA tile in `v0` are hardcoded UI.

### `v0/edit_profile.png` — Profile · `v0/contact.png` — Support

Department, address, GPA, credits earned, academic standing, advisor, enrollment type,
grade-alert and course-announcement toggles, support ticket (category, urgency, subject,
message) — **none of these have any table.** Both screens are unimplementable as drawn.

---

## 2. Cross-cutting schema problems

1. **No enrollment entity.** This single omission causes most of the wrong data above:
   the enrolled count, the student dashboard, the "Pending" row, the roster size, and the
   403 on an ungraded course all trace back to `scores` doubling as the roster.

2. **`scores.section` is stored at the wrong grain.** Section is a property of a class
   roster, but it is written on every (student × assignment) row — one duplicate per
   assignment per student, re-written by every CSV import, with nothing keeping the copies
   consistent.

3. **Profile columns are duplicated.** `first_name`, `middle_name`, `last_name`,
   `avatar_url`, `created_at` exist identically in `students` and `teachers`, forcing every
   consumer (`/me`, the grade sheet, the course card) to branch on which table to read.

4. **External identifiers used as primary keys.** `students.student_id` is the university
   ID and is propagated into `scores`. Correcting a mistyped student number means updating
   every child row.

5. **Soft delete is inconsistent and easy to forget.** `is_deleted` on courses, quizzes and
   scores; `is_archive` only on courses; nothing on students, teachers or uploads. Several
   queries omit the filter (see the student dashboard above). Deletion state is spread over
   two booleans with no timestamp and no record of who deleted.

6. **Missing constraints.**
   - No `UNIQUE (provider, provider_user_id)` on `auth_providers`.
   - No `UNIQUE` on `courses.course_id`, `students.auth_user_id`, `teachers.auth_user_id`.
   - No `CHECK` on `scores.score` (any float is accepted, including negatives and values
     above `full_mark`), on `quizzes.full_mark > 0`, or on `weight >= 0`.
   - `UNIQUE (student_id, quiz_id)` on `scores` ignores `is_deleted`, so a soft-deleted
     score permanently blocks re-adding that student to that assignment.
   - Relationships declare `passive_deletes=True` but the columns declare no
     `ondelete=` — no `ON DELETE` clause is emitted, so the database will refuse the
     delete rather than cascade.

7. **No indexes for the actual access paths.** Every hot query filters
   `WHERE quiz_id = ? AND is_deleted = false` or `WHERE student_id = ?`; only the primary
   keys are indexed.

8. **No migration tooling.** The app calls `Base.metadata.create_all()` at import
   (`fastapi/app/__init__.py:99`), which creates missing tables and never alters an
   existing one. Any column added from here on silently fails to appear in a database that
   already has the table.

9. **CSV import correctness.** `upload_csv()` matches students with
   `student_id.in_(ids) AND email.in_(emails)` (`teacher.py:216`) — a cross product, not a
   pairwise match, so a row can be matched against another row's email. `name.split()`
   raises `IndexError` on a single-word name, and the whole import is one transaction with
   no per-row error reporting.

---

## 3. What the redesign has to deliver

- An explicit **enrollment** entity, so the roster exists independently of grades.
- A **term / offering / section** structure, so the semester UI and repeated course
  offerings work.
- One **users** table, so profile data is stored once and role is explicit.
- **Assessments** with type, description, due date and ordering.
- **Scores keyed by enrollment**, with a read receipt, a grader and an audit trail.
- **Import batches** linked to the assessment they populated.
- **Cached statistics**, so the distribution screen stops scanning.
- Consistent soft delete, real constraints, and indexes matching the query patterns.

→ see [`er-model-v2.md`](./er-model-v2.md) and [`schema_v2.sql`](./schema_v2.sql).
