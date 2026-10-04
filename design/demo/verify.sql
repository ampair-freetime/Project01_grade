-- Read-only PostgreSQL verification. Run each section at its matching demo step.
-- If section B returns more than one course, resolve the demo course selection before continuing.


-- A: accounts; expected teacher + 5 students after live signup (no password column).
SELECT a.email, s.student_id,
       COALESCE(s.first_name, t.first_name) AS first_name,
       COALESCE(s.last_name, t.last_name) AS last_name,
       CASE WHEN s.student_id IS NOT NULL THEN 'student' ELSE 'teacher' END AS role
FROM auth_users a LEFT JOIN students s ON s.auth_user_id = a.auth_user_id
LEFT JOIN teachers t ON t.auth_user_id = a.auth_user_id
WHERE a.email IN ('demo.teacher@cmu.ac.th', 'demo_one@cmu.ac.th',
 'demo_two@cmu.ac.th', 'demo_three@cmu.ac.th', 'demo_four@cmu.ac.th', 'demo_five@cmu.ac.th')
ORDER BY a.email;


WITH demo_course AS (
    SELECT c.course_code FROM courses c
    JOIN teachers t ON t.teacher_id = c.teacher_id
    JOIN auth_users a ON a.auth_user_id = t.auth_user_id
    WHERE c.course_id = 'DEMO321' AND a.email = 'demo.teacher@cmu.ac.th'
)
-- B: expected one demo course; capture course_code and generated join_code.
SELECT c.course_code, c.course_id, c.course_name, c.section, c.teacher_id,
       c.join_code, c.join_open, c.is_archive, c.is_deleted
FROM courses c JOIN demo_course d ON d.course_code = c.course_code;


WITH demo_course AS (
    SELECT c.course_code FROM courses c
    JOIN teachers t ON t.teacher_id = c.teacher_id
    JOIN auth_users a ON a.auth_user_id = t.auth_user_id
    WHERE c.course_id = 'DEMO321' AND a.email = 'demo.teacher@cmu.ac.th'
)
-- C: expected 1 enrollment after join; 5 after CSV import.
SELECT e.enrollment_id, e.student_id, e.course_code, e.section,
       COALESCE(e.section, c.section) AS displayed_section, e.status, e.joined_via
FROM enrollments e JOIN demo_course d ON d.course_code = e.course_code
JOIN courses c ON c.course_code = e.course_code
ORDER BY e.student_id;


WITH demo_course AS (
    SELECT c.course_code FROM courses c
    JOIN teachers t ON t.teacher_id = c.teacher_id
    JOIN auth_users a ON a.auth_user_id = t.auth_user_id
    WHERE c.course_id = 'DEMO321' AND a.email = 'demo.teacher@cmu.ac.th'
)
-- D: quiz IDs and publication/deletion state.
SELECT q.quiz_id, q.quiz_name, q.full_mark, q.weight, q.is_publish, q.is_deleted
FROM quizzes q JOIN demo_course d ON d.course_code = q.course_code
ORDER BY q.quiz_name, q.quiz_id;


WITH demo_course AS (
    SELECT c.course_code FROM courses c
    JOIN teachers t ON t.teacher_id = c.teacher_id
    JOIN auth_users a ON a.auth_user_id = t.auth_user_id
    WHERE c.course_id = 'DEMO321' AND a.email = 'demo.teacher@cmu.ac.th'
)
-- E: main scores and read state. Record score_id before and after reimport.
SELECT s.score_id, s.student_id, a.email, s.score, s.unread_flag,
       s.is_deleted, s.updated_at, q.quiz_id
FROM scores s JOIN quizzes q ON q.quiz_id = s.quiz_id
JOIN demo_course d ON d.course_code = q.course_code
JOIN students st ON st.student_id = s.student_id
JOIN auth_users a ON a.auth_user_id = st.auth_user_id
WHERE q.quiz_name = 'Midterm' AND q.is_deleted = false
ORDER BY s.student_id;


WITH demo_course AS (
    SELECT c.course_code FROM courses c
    JOIN teachers t ON t.teacher_id = c.teacher_id
    JOIN auth_users a ON a.auth_user_id = t.auth_user_id
    WHERE c.course_id = 'DEMO321' AND a.email = 'demo.teacher@cmu.ac.th'
)
-- F: import log. uploads does not store quiz_id in the current model.
SELECT u.upload_id, u.file_name, u.course_code, u.created_at
FROM uploads u JOIN demo_course d ON d.course_code = u.course_code
ORDER BY u.created_at, u.upload_id;


WITH demo_course AS (
    SELECT c.course_code FROM courses c
    JOIN teachers t ON t.teacher_id = c.teacher_id
    JOIN auth_users a ON a.auth_user_id = t.auth_user_id
    WHERE c.course_id = 'DEMO321' AND a.email = 'demo.teacher@cmu.ac.th'
)
, main_scores AS (
 SELECT s.quiz_id, s.student_id, s.score FROM scores s
 JOIN quizzes q ON q.quiz_id = s.quiz_id
 JOIN demo_course d ON d.course_code = q.course_code
 WHERE q.quiz_name = 'Midterm' AND q.is_deleted = false AND s.is_deleted = false
)
-- G: population std matches backend. Expected after update: 5,81,85,14.28,100,60.
SELECT quiz_id, COUNT(*) AS total_students,
 ROUND(AVG(score)::numeric, 2) AS mean,
 ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY score))::numeric, 2) AS median,
 ROUND(STDDEV_POP(score)::numeric, 2) AS std,
 MAX(score) AS highest, MIN(score) AS lowest
FROM main_scores GROUP BY quiz_id;


WITH demo_course AS (
    SELECT c.course_code FROM courses c
    JOIN teachers t ON t.teacher_id = c.teacher_id
    JOIN auth_users a ON a.auth_user_id = t.auth_user_id
    WHERE c.course_id = 'DEMO321' AND a.email = 'demo.teacher@cmu.ac.th'
)
-- G2: percent/rank for Demo Three; expected 85%, rank 3.
SELECT s.student_id, s.score, q.full_mark,
 ROUND((s.score / NULLIF(q.full_mark, 0) * 100)::numeric, 2) AS percent,
 1 + (SELECT COUNT(*) FROM scores higher
      WHERE higher.quiz_id = s.quiz_id AND higher.is_deleted = false
        AND higher.score > s.score) AS ranking
FROM scores s JOIN quizzes q ON q.quiz_id = s.quiz_id
JOIN demo_course d ON d.course_code = q.course_code
WHERE q.quiz_name = 'Midterm' AND q.is_deleted = false
 AND s.student_id = '690510903' AND s.is_deleted = false;


WITH demo_course AS (
    SELECT c.course_code FROM courses c
    JOIN teachers t ON t.teacher_id = c.teacher_id
    JOIN auth_users a ON a.auth_user_id = t.auth_user_id
    WHERE c.course_id = 'DEMO321' AND a.email = 'demo.teacher@cmu.ac.th'
)
-- G3: published weighted average; expected 85.00 with only Midterm published.
SELECT q.course_code,
 ROUND((100.0 * SUM(CASE WHEN s.score IS NOT NULL AND q.full_mark > 0
       THEN s.score / q.full_mark * q.weight ELSE 0 END)
       / NULLIF(SUM(q.weight), 0))::numeric, 2) AS weighted_average
FROM quizzes q JOIN demo_course d ON d.course_code = q.course_code
LEFT JOIN scores s ON s.quiz_id = q.quiz_id AND s.student_id = '690510903'
 AND s.is_deleted = false
WHERE q.is_deleted = false AND q.is_publish = true
GROUP BY q.course_code;


WITH demo_course AS (
    SELECT c.course_code FROM courses c
    JOIN teachers t ON t.teacher_id = c.teacher_id
    JOIN auth_users a ON a.auth_user_id = t.auth_user_id
    WHERE c.course_id = 'DEMO321' AND a.email = 'demo.teacher@cmu.ac.th'
)
-- H1: physical rows retained after soft delete (expect is_deleted=true).
SELECT q.quiz_id, q.quiz_name, q.is_deleted AS quiz_deleted,
       s.score_id, s.student_id, s.score, s.is_deleted AS score_deleted
FROM quizzes q JOIN demo_course d ON d.course_code = q.course_code
LEFT JOIN scores s ON s.quiz_id = q.quiz_id
WHERE q.quiz_name = 'Practice Delete';


WITH demo_course AS (
    SELECT c.course_code FROM courses c
    JOIN teachers t ON t.teacher_id = c.teacher_id
    JOIN auth_users a ON a.auth_user_id = t.auth_user_id
    WHERE c.course_id = 'DEMO321' AND a.email = 'demo.teacher@cmu.ac.th'
)
-- H2: after score deletion, expected no active practice score.
SELECT s.score_id, s.student_id, s.score
FROM scores s JOIN quizzes q ON q.quiz_id = s.quiz_id
JOIN demo_course d ON d.course_code = q.course_code
WHERE q.quiz_name = 'Practice Delete' AND s.is_deleted = false;


WITH demo_course AS (
    SELECT c.course_code FROM courses c
    JOIN teachers t ON t.teacher_id = c.teacher_id
    JOIN auth_users a ON a.auth_user_id = t.auth_user_id
    WHERE c.course_id = 'DEMO321' AND a.email = 'demo.teacher@cmu.ac.th'
)
-- H3: after assignment deletion, expected no active practice assignment.
SELECT q.quiz_id, q.quiz_name FROM quizzes q
JOIN demo_course d ON d.course_code = q.course_code
WHERE q.quiz_name = 'Practice Delete' AND q.is_deleted = false;
