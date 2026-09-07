-- =====================================================================
-- Exam Score Portal — schema v2 (PostgreSQL 13+)
-- Companion to design/database/er-model-v2.md
--
-- Layers:
--   1. identity        users, auth_identities
--   2. catalogue       terms, courses, sections, section_instructors
--   3. roster          enrollments
--   4. assessment      assessments, scores
--   5. operations      score_audits, score_imports, assessment_stats
--   6. optional        grade_bands, notifications, support_tickets, user_preferences
-- =====================================================================

BEGIN;

-- gen_random_uuid() is core in PostgreSQL 13+.

-- ---------------------------------------------------------------------
-- 0. enum types
-- ---------------------------------------------------------------------
CREATE TYPE user_role         AS ENUM ('student', 'teacher', 'admin');
CREATE TYPE user_status       AS ENUM ('invited', 'active', 'disabled');
CREATE TYPE section_status    AS ENUM ('draft', 'active', 'archived');
CREATE TYPE instructor_role   AS ENUM ('owner', 'co_teacher', 'ta');
CREATE TYPE enrollment_status AS ENUM ('active', 'dropped', 'completed');
CREATE TYPE assessment_kind   AS ENUM ('exam', 'quiz', 'assignment', 'project', 'participation', 'other');
CREATE TYPE publish_status    AS ENUM ('draft', 'published');
CREATE TYPE score_status      AS ENUM ('pending', 'graded', 'excused');
CREATE TYPE import_status     AS ENUM ('pending', 'processing', 'completed', 'failed');


-- =====================================================================
-- 1. IDENTITY
-- =====================================================================

-- One row per person. Replaces auth_users + the duplicated name/avatar
-- columns of students and teachers.
CREATE TABLE users (
    user_id       UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    email         TEXT        NOT NULL,
    password_hash TEXT,                                   -- NULL while status = 'invited'
    role          user_role   NOT NULL,
    status        user_status NOT NULL DEFAULT 'invited',

    first_name    VARCHAR(100) NOT NULL,
    middle_name   VARCHAR(100),
    last_name     VARCHAR(100) NOT NULL,
    avatar_url    VARCHAR(500),

    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_login_at TIMESTAMPTZ,
    deleted_at    TIMESTAMPTZ,

    CONSTRAINT users_email_format_chk CHECK (position('@' IN email) > 1),
    -- an active account must be able to authenticate somehow; identity rows
    -- cover OAuth-only accounts, so this is enforced in the app, not here.
    CONSTRAINT users_active_needs_name_chk
        CHECK (status <> 'active' OR length(btrim(first_name)) > 0)
);
CREATE UNIQUE INDEX users_email_uidx ON users (lower(email)) WHERE deleted_at IS NULL;
CREATE INDEX users_role_idx ON users (role) WHERE deleted_at IS NULL;

-- Student-only attributes. 1:1 optional extension of users.
CREATE TABLE student_profiles (
    user_id      UUID PRIMARY KEY REFERENCES users (user_id) ON DELETE CASCADE,
    student_no   VARCHAR(20) NOT NULL,                     -- university ID, an attribute now
    program      VARCHAR(150),                             -- "Computer Science"
    year_level   SMALLINT,
    advisor_id   UUID REFERENCES users (user_id) ON DELETE SET NULL,
    CONSTRAINT student_profiles_year_chk CHECK (year_level IS NULL OR year_level BETWEEN 1 AND 12)
);
CREATE UNIQUE INDEX student_profiles_no_uidx ON student_profiles (student_no);

-- Teacher-only attributes.
CREATE TABLE teacher_profiles (
    user_id    UUID PRIMARY KEY REFERENCES users (user_id) ON DELETE CASCADE,
    staff_no   VARCHAR(20),
    department VARCHAR(150),
    title      VARCHAR(50)                                 -- "Prof.", "Dr."
);
CREATE UNIQUE INDEX teacher_profiles_staff_no_uidx ON teacher_profiles (staff_no) WHERE staff_no IS NOT NULL;

-- Federated logins. Replaces auth_providers, with the uniqueness the
-- Google callback already assumes.
CREATE TABLE auth_identities (
    identity_id      UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id          UUID        NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
    provider         VARCHAR(50) NOT NULL,                 -- 'google', 'microsoft', ...
    provider_user_id VARCHAR(255) NOT NULL,
    email_at_provider TEXT,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_used_at     TIMESTAMPTZ,

    CONSTRAINT auth_identities_provider_uq UNIQUE (provider, provider_user_id),
    CONSTRAINT auth_identities_one_per_provider_uq UNIQUE (user_id, provider)
);


-- =====================================================================
-- 2. CATALOGUE
-- =====================================================================

-- Academic term. Drives every "Fall 2023" / "Spring 2024" label and the
-- semester dropdown.
CREATE TABLE terms (
    term_id       SMALLSERIAL PRIMARY KEY,
    code          VARCHAR(20) NOT NULL,                    -- '2023F'
    name          VARCHAR(50) NOT NULL,                    -- 'Fall 2023'
    academic_year SMALLINT    NOT NULL,
    starts_on     DATE        NOT NULL,
    ends_on       DATE        NOT NULL,

    CONSTRAINT terms_code_uq   UNIQUE (code),
    CONSTRAINT terms_dates_chk CHECK (ends_on > starts_on)
);
CREATE INDEX terms_range_idx ON terms (starts_on, ends_on);

-- Catalogue entry: the subject itself, independent of who teaches it or when.
-- Title and description are stored once, not once per semester.
CREATE TABLE courses (
    course_id   UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    code        VARCHAR(20) NOT NULL,                      -- 'CS101' — what the UI calls Course Code
    title       VARCHAR(255) NOT NULL,                     -- 'Intro to Computer Science'
    description TEXT,
    credits     NUMERIC(3,1),
    department  VARCHAR(150),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at  TIMESTAMPTZ
);
CREATE UNIQUE INDEX courses_code_uidx ON courses (upper(code)) WHERE deleted_at IS NULL;

-- One course, one term, one section — the card on Course Management and
-- the thing a student actually enrols in.
CREATE TABLE sections (
    section_id    UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id     UUID           NOT NULL REFERENCES courses (course_id) ON DELETE RESTRICT,
    term_id       SMALLINT       NOT NULL REFERENCES terms (term_id)     ON DELETE RESTRICT,
    section_code  VARCHAR(10)    NOT NULL DEFAULT '001',   -- 'A', '001' — was scores.section
    schedule_note VARCHAR(255),                            -- 'Mon/Wed 10:00–11:30'
    capacity      SMALLINT,
    status        section_status NOT NULL DEFAULT 'active',

    created_by    UUID           REFERENCES users (user_id) ON DELETE SET NULL,
    created_at    TIMESTAMPTZ    NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ    NOT NULL DEFAULT now(),
    archived_at   TIMESTAMPTZ,
    deleted_at    TIMESTAMPTZ,

    CONSTRAINT sections_identity_uq UNIQUE (course_id, term_id, section_code),
    CONSTRAINT sections_capacity_chk CHECK (capacity IS NULL OR capacity > 0),
    CONSTRAINT sections_archived_chk CHECK ((status = 'archived') = (archived_at IS NOT NULL))
);
CREATE INDEX sections_term_idx   ON sections (term_id, status) WHERE deleted_at IS NULL;
CREATE INDEX sections_course_idx ON sections (course_id)       WHERE deleted_at IS NULL;

-- Who may teach / grade a section. A junction table instead of a single
-- teacher_id column, so co-teachers and TAs need no schema change.
CREATE TABLE section_instructors (
    section_id UUID            NOT NULL REFERENCES sections (section_id) ON DELETE CASCADE,
    user_id    UUID            NOT NULL REFERENCES users (user_id)       ON DELETE RESTRICT,
    role       instructor_role NOT NULL DEFAULT 'owner',
    added_at   TIMESTAMPTZ     NOT NULL DEFAULT now(),

    PRIMARY KEY (section_id, user_id)
);
CREATE INDEX section_instructors_user_idx ON section_instructors (user_id);
-- exactly one owner per section
CREATE UNIQUE INDEX section_instructors_owner_uidx
    ON section_instructors (section_id) WHERE role = 'owner';


-- =====================================================================
-- 3. ROSTER
-- =====================================================================

-- The missing entity of v1. The roster now exists before any grade does.
CREATE TABLE enrollments (
    enrollment_id UUID              PRIMARY KEY DEFAULT gen_random_uuid(),
    section_id    UUID              NOT NULL REFERENCES sections (section_id) ON DELETE CASCADE,
    student_id    UUID              NOT NULL REFERENCES users (user_id)       ON DELETE RESTRICT,
    status        enrollment_status NOT NULL DEFAULT 'active',
    enrolled_at   TIMESTAMPTZ       NOT NULL DEFAULT now(),
    dropped_at    TIMESTAMPTZ,
    final_percent NUMERIC(5,2),                            -- cached weighted average
    final_grade   VARCHAR(5),                              -- 'A', 'B+' (see grade_bands)

    CONSTRAINT enrollments_uq          UNIQUE (section_id, student_id),
    CONSTRAINT enrollments_dropped_chk CHECK ((status = 'dropped') = (dropped_at IS NOT NULL)),
    CONSTRAINT enrollments_percent_chk CHECK (final_percent IS NULL OR final_percent BETWEEN 0 AND 100)
);
CREATE INDEX enrollments_student_idx ON enrollments (student_id, status);
CREATE INDEX enrollments_section_idx ON enrollments (section_id, status);


-- =====================================================================
-- 4. ASSESSMENT
-- =====================================================================

-- Was `quizzes`. Renamed to the word every screen uses, and given the
-- attributes the mockups display.
CREATE TABLE assessments (
    assessment_id UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    section_id    UUID            NOT NULL REFERENCES sections (section_id) ON DELETE CASCADE,
    title         VARCHAR(255)    NOT NULL,                -- 'Midterm Exam'
    description   VARCHAR(500),                            -- 'In-class written exam'
    kind          assessment_kind NOT NULL DEFAULT 'assignment',
    full_mark     NUMERIC(6,2)    NOT NULL DEFAULT 100,
    weight        NUMERIC(5,2)    NOT NULL DEFAULT 0,      -- percent of the final grade
    due_at        TIMESTAMPTZ,
    position      SMALLINT        NOT NULL DEFAULT 0,      -- display order

    status        publish_status  NOT NULL DEFAULT 'draft',
    published_at  TIMESTAMPTZ,
    published_by  UUID            REFERENCES users (user_id) ON DELETE SET NULL,

    created_by    UUID            REFERENCES users (user_id) ON DELETE SET NULL,
    created_at    TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ     NOT NULL DEFAULT now(),
    deleted_at    TIMESTAMPTZ,

    CONSTRAINT assessments_full_mark_chk CHECK (full_mark > 0),
    CONSTRAINT assessments_weight_chk    CHECK (weight >= 0 AND weight <= 100),
    CONSTRAINT assessments_publish_chk   CHECK ((status = 'published') = (published_at IS NOT NULL))
);
CREATE INDEX assessments_section_idx ON assessments (section_id, position) WHERE deleted_at IS NULL;
CREATE INDEX assessments_published_idx ON assessments (section_id)
    WHERE deleted_at IS NULL AND status = 'published';
-- one title per section, ignoring soft-deleted rows
CREATE UNIQUE INDEX assessments_title_uidx
    ON assessments (section_id, lower(title)) WHERE deleted_at IS NULL;

-- One row per (assessment, enrolled student). Keyed by enrollment, so a
-- score for a student who is not on the roster is impossible by construction.
CREATE TABLE scores (
    score_id      UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id UUID         NOT NULL REFERENCES assessments (assessment_id) ON DELETE CASCADE,
    enrollment_id UUID         NOT NULL REFERENCES enrollments (enrollment_id) ON DELETE CASCADE,

    points        NUMERIC(6,2),                            -- NULL = not graded yet
    status        score_status NOT NULL DEFAULT 'pending',
    remark        VARCHAR(500),                            -- per-student feedback

    graded_by     UUID         REFERENCES users (user_id) ON DELETE SET NULL,
    graded_at     TIMESTAMPTZ,
    viewed_at     TIMESTAMPTZ,                             -- replaces unread_flag
    import_id     UUID,                                    -- FK added after score_imports

    created_at    TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ  NOT NULL DEFAULT now(),
    deleted_at    TIMESTAMPTZ,

    CONSTRAINT scores_points_chk  CHECK (points IS NULL OR points >= 0),
    CONSTRAINT scores_graded_chk  CHECK ((status = 'graded') = (points IS NOT NULL))
);
-- one score per student per assessment, and a soft-deleted row no longer
-- blocks re-entry (the v1 constraint did)
CREATE UNIQUE INDEX scores_uidx
    ON scores (assessment_id, enrollment_id) WHERE deleted_at IS NULL;
CREATE INDEX scores_enrollment_idx ON scores (enrollment_id) WHERE deleted_at IS NULL;
-- powers the "NEW GRADE" badge and the Unread filter without a table scan
CREATE INDEX scores_unread_idx ON scores (enrollment_id)
    WHERE viewed_at IS NULL AND deleted_at IS NULL AND status = 'graded';

-- points <= assessments.full_mark is a cross-table rule; PostgreSQL cannot
-- express it as a CHECK, so it is a trigger.
CREATE OR REPLACE FUNCTION scores_within_full_mark() RETURNS TRIGGER AS $$
DECLARE
    max_points NUMERIC(6,2);
BEGIN
    IF NEW.points IS NULL THEN
        RETURN NEW;
    END IF;
    SELECT full_mark INTO max_points FROM assessments WHERE assessment_id = NEW.assessment_id;
    IF NEW.points > max_points THEN
        RAISE EXCEPTION 'score % exceeds full mark % for assessment %',
            NEW.points, max_points, NEW.assessment_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER scores_within_full_mark_trg
    BEFORE INSERT OR UPDATE OF points, assessment_id ON scores
    FOR EACH ROW EXECUTE FUNCTION scores_within_full_mark();

-- the assessment and the enrollment must belong to the same section
CREATE OR REPLACE FUNCTION scores_same_section() RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT section_id FROM assessments WHERE assessment_id = NEW.assessment_id)
       IS DISTINCT FROM
       (SELECT section_id FROM enrollments WHERE enrollment_id = NEW.enrollment_id)
    THEN
        RAISE EXCEPTION 'assessment and enrollment belong to different sections';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER scores_same_section_trg
    BEFORE INSERT OR UPDATE OF assessment_id, enrollment_id ON scores
    FOR EACH ROW EXECUTE FUNCTION scores_same_section();


-- =====================================================================
-- 5. OPERATIONS
-- =====================================================================

-- Grade change log. Backs "Last updated by", grade appeals and the
-- "Grading Issues" support topic.
CREATE TABLE score_audits (
    audit_id   BIGSERIAL    PRIMARY KEY,
    score_id   UUID         NOT NULL REFERENCES scores (score_id) ON DELETE CASCADE,
    changed_by UUID         REFERENCES users (user_id) ON DELETE SET NULL,
    old_points NUMERIC(6,2),
    new_points NUMERIC(6,2),
    reason     VARCHAR(255),
    source     VARCHAR(20)  NOT NULL DEFAULT 'manual',     -- 'manual' | 'csv' | 'api'
    changed_at TIMESTAMPTZ  NOT NULL DEFAULT now()
);
CREATE INDEX score_audits_score_idx ON score_audits (score_id, changed_at DESC);

-- One CSV upload. Replaces `uploads`, and — unlike it — records which
-- assessment was populated, so an import can be reviewed or rolled back.
CREATE TABLE score_imports (
    import_id     UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id UUID          NOT NULL REFERENCES assessments (assessment_id) ON DELETE CASCADE,
    uploaded_by   UUID          REFERENCES users (user_id) ON DELETE SET NULL,

    file_name     VARCHAR(255)  NOT NULL,
    file_size     INTEGER,
    storage_key   VARCHAR(500),                            -- object-storage path, if kept
    checksum      CHAR(64),                                -- sha256, to detect a re-upload

    status        import_status NOT NULL DEFAULT 'pending',
    row_count     INTEGER       NOT NULL DEFAULT 0,
    success_count INTEGER       NOT NULL DEFAULT 0,
    error_count   INTEGER       NOT NULL DEFAULT 0,
    errors        JSONB,                                   -- [{row, column, message}, ...]

    created_at    TIMESTAMPTZ   NOT NULL DEFAULT now(),
    completed_at  TIMESTAMPTZ,

    CONSTRAINT score_imports_counts_chk CHECK (success_count + error_count <= row_count)
);
CREATE INDEX score_imports_assessment_idx ON score_imports (assessment_id, created_at DESC);

ALTER TABLE scores
    ADD CONSTRAINT scores_import_fk
    FOREIGN KEY (import_id) REFERENCES score_imports (import_id) ON DELETE SET NULL;

-- Cached class statistics. Recomputed when scores are saved or published,
-- so the student score screen stops recomputing σ from every row per view.
CREATE TABLE assessment_stats (
    assessment_id  UUID        PRIMARY KEY REFERENCES assessments (assessment_id) ON DELETE CASCADE,
    graded_count   INTEGER     NOT NULL DEFAULT 0,
    enrolled_count INTEGER     NOT NULL DEFAULT 0,
    mean_points    NUMERIC(6,2),
    median_points  NUMERIC(6,2),
    stddev_points  NUMERIC(6,2),
    min_points     NUMERIC(6,2),
    max_points     NUMERIC(6,2),
    computed_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);


-- =====================================================================
-- 6. OPTIONAL — drop any of these without touching the core
-- =====================================================================

-- Letter grade / GPA bands, per section (v0/GPA.png "GRADE A").
CREATE TABLE grade_bands (
    band_id     BIGSERIAL    PRIMARY KEY,
    section_id  UUID         NOT NULL REFERENCES sections (section_id) ON DELETE CASCADE,
    letter      VARCHAR(5)   NOT NULL,                     -- 'A', 'B+'
    min_percent NUMERIC(5,2) NOT NULL,
    grade_point NUMERIC(3,2) NOT NULL,                     -- 4.00

    CONSTRAINT grade_bands_uq          UNIQUE (section_id, letter),
    CONSTRAINT grade_bands_percent_chk CHECK (min_percent BETWEEN 0 AND 100)
);

-- Notification bell (v0/teacher_courses.png, v1/popup_create.png).
CREATE TABLE notifications (
    notification_id BIGSERIAL   PRIMARY KEY,
    user_id         UUID        NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
    kind            VARCHAR(50) NOT NULL,                  -- 'grade_published', 'course_announcement'
    title           VARCHAR(255) NOT NULL,
    body            VARCHAR(500),
    link_url        VARCHAR(500),
    read_at         TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX notifications_unread_idx ON notifications (user_id, created_at DESC) WHERE read_at IS NULL;

-- Per-user toggles (v0/edit_profile.png "Grade Alerts").
CREATE TABLE user_preferences (
    user_id            UUID    PRIMARY KEY REFERENCES users (user_id) ON DELETE CASCADE,
    notify_grade       BOOLEAN NOT NULL DEFAULT true,
    notify_announcement BOOLEAN NOT NULL DEFAULT true,
    theme              VARCHAR(10) NOT NULL DEFAULT 'system',
    locale             VARCHAR(10) NOT NULL DEFAULT 'th'
);

-- Support form (v0/contact.png).
CREATE TABLE support_tickets (
    ticket_id  BIGSERIAL    PRIMARY KEY,
    user_id    UUID         REFERENCES users (user_id) ON DELETE SET NULL,
    category   VARCHAR(50)  NOT NULL,                      -- 'grading', 'technical', 'admin'
    urgency    VARCHAR(20)  NOT NULL DEFAULT 'normal',
    subject    VARCHAR(255) NOT NULL,
    message    TEXT         NOT NULL,
    status     VARCHAR(20)  NOT NULL DEFAULT 'open',
    section_id UUID         REFERENCES sections (section_id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ  NOT NULL DEFAULT now(),
    resolved_at TIMESTAMPTZ
);
CREATE INDEX support_tickets_user_idx ON support_tickets (user_id, created_at DESC);


-- =====================================================================
-- 7. VIEWS — make the soft-delete filter impossible to forget
-- =====================================================================

CREATE VIEW v_active_sections AS
    SELECT s.*, c.code AS course_code, c.title AS course_title, t.name AS term_name
      FROM sections s
      JOIN courses  c ON c.course_id = s.course_id
      JOIN terms    t ON t.term_id   = s.term_id
     WHERE s.deleted_at IS NULL AND s.status <> 'archived';

CREATE VIEW v_active_assessments AS
    SELECT * FROM assessments WHERE deleted_at IS NULL;

-- The teacher grade sheet: every enrolled student, graded or not.
-- This is the query v1 could not express.
CREATE VIEW v_grade_sheet AS
    SELECT a.assessment_id,
           a.section_id,
           e.enrollment_id,
           u.user_id,
           sp.student_no,
           u.first_name, u.middle_name, u.last_name, u.avatar_url,
           sec.section_code,
           s.score_id,
           s.points,
           COALESCE(s.status, 'pending')          AS score_status,
           (s.viewed_at IS NOT NULL)              AS is_read,
           s.updated_at                           AS last_updated
      FROM assessments a
      JOIN sections    sec ON sec.section_id = a.section_id
      JOIN enrollments e   ON e.section_id   = a.section_id AND e.status = 'active'
      JOIN users       u   ON u.user_id      = e.student_id
      LEFT JOIN student_profiles sp ON sp.user_id = u.user_id
      LEFT JOIN scores s   ON s.assessment_id = a.assessment_id
                          AND s.enrollment_id = e.enrollment_id
                          AND s.deleted_at IS NULL
     WHERE a.deleted_at IS NULL;

-- Enrolled headcount per section, for the "142 STUDENTS" column.
CREATE VIEW v_section_enrollment_counts AS
    SELECT section_id, count(*) AS enrolled_count
      FROM enrollments
     WHERE status = 'active'
     GROUP BY section_id;

COMMIT;
