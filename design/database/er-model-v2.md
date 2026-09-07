# ER Model v2 — Exam Score Portal

Redesign of the database behind `design/ui/`. Motivated by the gaps recorded in
[`ui-db-review.md`](./ui-db-review.md); the executable form is
[`schema_v2.sql`](./schema_v2.sql).

---

## 1. The five changes that matter

| # | Change | Fixes |
|---|---|---|
| 1 | **`enrollments` becomes a real entity** | The roster no longer *is* the score table. Enrolled counts, the "Pending / `--`" row, the student dashboard and the 403-before-first-grade all become correct. |
| 2 | **`terms` + `courses` + `sections`** replace one flat `courses` table | The semester UI works; a course title is stored once instead of once per offering; `section` stops being copied onto every score row. |
| 3 | **One `users` table** with `role`, plus thin 1:1 profile tables | Name/avatar/created_at stop being duplicated across `students` and `teachers`; role stops being guessed from which relationship is non-null. |
| 4 | **`scores` keyed by `enrollment_id`** | Scoring a non-enrolled student becomes impossible by construction rather than by convention. |
| 5 | **`score_imports` + `score_audits` + `assessment_stats`** | CSV imports become reviewable, grade changes become traceable, and class statistics stop being recomputed from every row on every page view. |

---

## 2. Entity–relationship diagram

```mermaid
erDiagram
    users ||--o| student_profiles  : "is a"
    users ||--o| teacher_profiles  : "is a"
    users ||--o{ auth_identities   : "logs in via"

    terms   ||--o{ sections : "scheduled in"
    courses ||--o{ sections : "offered as"

    sections ||--o{ section_instructors : "taught by"
    users    ||--o{ section_instructors : "teaches"

    sections ||--o{ enrollments : "has roster"
    users    ||--o{ enrollments : "enrols in"

    sections    ||--o{ assessments : "contains"
    assessments ||--o{ scores      : "graded as"
    enrollments ||--o{ scores      : "receives"

    assessments ||--o| assessment_stats : "summarised by"
    assessments ||--o{ score_imports    : "populated by"
    score_imports ||--o{ scores         : "wrote"
    scores      ||--o{ score_audits     : "changed by"
    users       ||--o{ score_audits     : "made change"

    sections ||--o{ grade_bands     : "graded on"
    users    ||--o{ notifications   : "receives"
    users    ||--o| user_preferences: "configures"
    users    ||--o{ support_tickets : "opens"

    users {
        uuid        user_id PK
        text        email UK
        text        password_hash "null while invited"
        user_role   role "student|teacher|admin"
        user_status status "invited|active|disabled"
        varchar     first_name
        varchar     middle_name
        varchar     last_name
        varchar     avatar_url
        timestamptz deleted_at
    }
    student_profiles {
        uuid    user_id PK_FK
        varchar student_no UK "university ID — attribute, not PK"
        varchar program
        uuid    advisor_id FK
    }
    teacher_profiles {
        uuid    user_id PK_FK
        varchar department
        varchar title
    }
    auth_identities {
        uuid    identity_id PK
        uuid    user_id FK
        varchar provider "UK with provider_user_id"
        varchar provider_user_id
    }
    terms {
        smallint term_id PK
        varchar  code UK "2023F"
        varchar  name "Fall 2023"
        date     starts_on
        date     ends_on
    }
    courses {
        uuid    course_id PK
        varchar code UK "CS101"
        varchar title
        text    description
        numeric credits
    }
    sections {
        uuid           section_id PK
        uuid           course_id FK
        smallint       term_id FK
        varchar        section_code "A — was scores.section"
        varchar        schedule_note
        section_status status "draft|active|archived"
        timestamptz    deleted_at
    }
    section_instructors {
        uuid            section_id PK_FK
        uuid            user_id PK_FK
        instructor_role role "owner|co_teacher|ta"
    }
    enrollments {
        uuid              enrollment_id PK
        uuid              section_id FK "UK with student_id"
        uuid              student_id FK
        enrollment_status status "active|dropped|completed"
        numeric           final_percent
        varchar           final_grade
    }
    assessments {
        uuid            assessment_id PK
        uuid            section_id FK
        varchar         title
        varchar         description "In-class written exam"
        assessment_kind kind "exam|quiz|assignment|..."
        numeric         full_mark
        numeric         weight
        timestamptz     due_at
        smallint        position
        publish_status  status "draft|published"
        timestamptz     published_at
        timestamptz     deleted_at
    }
    scores {
        uuid         score_id PK
        uuid         assessment_id FK "UK with enrollment_id"
        uuid         enrollment_id FK
        numeric      points "null until graded"
        score_status status "pending|graded|excused"
        varchar      remark
        uuid         graded_by FK
        timestamptz  graded_at
        timestamptz  viewed_at "replaces unread_flag"
        uuid         import_id FK
        timestamptz  deleted_at
    }
    score_imports {
        uuid          import_id PK
        uuid          assessment_id FK "the link v1 lost"
        uuid          uploaded_by FK
        varchar       file_name
        import_status status
        integer       row_count
        integer       error_count
        jsonb         errors
    }
    score_audits {
        bigint      audit_id PK
        uuid        score_id FK
        uuid        changed_by FK
        numeric     old_points
        numeric     new_points
        varchar     source "manual|csv|api"
        timestamptz changed_at
    }
    assessment_stats {
        uuid    assessment_id PK_FK
        integer graded_count
        integer enrolled_count
        numeric mean_points
        numeric median_points
        numeric stddev_points
        numeric min_points
        numeric max_points
    }
    grade_bands {
        bigint  band_id PK
        uuid    section_id FK
        varchar letter "A, B+"
        numeric min_percent
        numeric grade_point
    }
    notifications {
        bigint      notification_id PK
        uuid        user_id FK
        varchar     kind
        timestamptz read_at
    }
    user_preferences {
        uuid    user_id PK_FK
        boolean notify_grade
        varchar theme
    }
    support_tickets {
        bigint  ticket_id PK
        uuid    user_id FK
        varchar category
        varchar urgency
        varchar subject
        varchar status
    }
```

---

## 3. Cardinalities and the reasoning behind them

| Relationship | Cardinality | Why |
|---|---|---|
| `users` → `student_profiles` / `teacher_profiles` | 1 : 0..1 | Role-specific columns live off the hot table; `/me` reads one row regardless of role. |
| `users` → `auth_identities` | 1 : 0..n, unique per provider | One account, one Google link, and `UNIQUE (provider, provider_user_id)` makes the callback's `.first()` lookup safe. |
| `courses` × `terms` → `sections` | m : n resolved by `sections` | `CS101` in Fall 2023 and in Spring 2024 are two sections of one catalogue row — the title is stored once. |
| `sections` ↔ `users` (teaching) | m : n via `section_instructors` | Supports co-teachers and TAs with no schema change; a partial unique index keeps exactly one `owner`. |
| `sections` ↔ `users` (studying) | m : n via `enrollments` | **The core fix.** The roster is independent of grading. |
| `sections` → `assessments` | 1 : n | Weights and assessments belong to a specific offering, not to the catalogue entry. |
| `assessments` × `enrollments` → `scores` | 1 : 1 per pair | `UNIQUE (assessment_id, enrollment_id)` as a *partial* index, so a soft-deleted score no longer blocks re-entry. |
| `scores` → `score_audits` | 1 : n | Append-only history for appeals. |
| `assessments` → `score_imports` | 1 : n | Import history per assessment; `scores.import_id` records which batch wrote each mark. |

**Referential integrity worth pointing at:** because `scores.enrollment_id` points at
`enrollments` rather than at a student, and a trigger checks that the assessment and the
enrollment share a `section_id`, a score for a student who is not on that section's roster
cannot be inserted at all. In v1 that rule existed only inside `upload_csv()`.

---

## 4. How each screen is served

| Screen | Tables read | Notes |
|---|---|---|
| `login`, `sign_up` | `users`, `auth_identities` | Role comes from `users.role`, set when the account is invited — not inferred from the form. |
| Teacher **Course Management** | `v_active_sections`, `v_section_enrollment_counts`, `terms` | Enrolled count from `enrollments`, not from scores. Term dropdown from `terms`. Section chip from `sections.section_code`. |
| **Create Course** dialog | `courses`, `terms`, `sections` | Now needs code + title + term + section code. |
| Teacher **Assignments** | `assessments` | `kind`, `description`, `due_at`, `position` fill the columns the mockups already show. |
| Teacher **Grade sheet** | `v_grade_sheet`, `assessment_stats` | Every active enrollment appears, graded or not — "Pending / `--`" becomes representable. Read/Unread from `scores.viewed_at`. Row count for "1–5 of 34" from `enrollments`. |
| **Import CSV** | `score_imports`, `scores`, `score_audits` | Batch is recorded before rows are applied; per-row failures land in `errors` instead of aborting the request. |
| **Publish Scores** | `assessments.status/published_at/published_by` | Publish becomes a timestamped, attributable event. |
| Student **Dashboard** | `enrollments` → `sections` → `courses`/`terms`, `section_instructors` | Courses come from the roster, so a course appears the moment the student is enrolled. "NEW GRADE" = `EXISTS` on the `scores_unread_idx` partial index. |
| Student **Course detail** | `assessments`, `scores`, `enrollments.final_percent` | Description and weight per row; weighted average cached on the enrollment. |
| Student **Score detail** | `scores`, `assessment_stats` | Mean/median/σ/min/max read from one cached row instead of scanning the class. |
| `v0` **GPA / letter grade** | `grade_bands`, `enrollments.final_grade` | Grading scale is data, not hardcoded UI. |
| `v0` **Profile** | `users`, `student_profiles`, `user_preferences` | Department, program, advisor, notification toggles. |
| `v0` **Support** | `support_tickets` | Category, urgency, subject, message from the form. |

---

## 5. Conventions applied throughout

- **Soft delete is one column, `deleted_at TIMESTAMPTZ`**, on every table that has it —
  never a mix of `is_deleted` and `is_archive`. Archiving is a separate, explicit
  `sections.status = 'archived'` + `archived_at`. Views (`v_active_sections`,
  `v_active_assessments`) hand out pre-filtered rows so the filter cannot be forgotten.
- **Surrogate UUID primary keys everywhere**; external identifiers (`student_no`,
  `courses.code`, `terms.code`) are unique *attributes*. A corrected student number is now
  a one-row update.
- **State is an enum, never an inferred null.** `users.status = 'invited'` replaces
  "password IS NULL means invited"; `scores.status` distinguishes pending from excused
  from graded.
- **Unique indexes are partial** (`WHERE deleted_at IS NULL`) so soft-deleted rows never
  block a legitimate insert.
- **Every FK declares `ON DELETE`.** `RESTRICT` for anything a person owns (a user with
  grades cannot vanish), `CASCADE` for dependent detail (a section's assessments and
  roster), `SET NULL` for attribution (`graded_by`, `created_by`).
- **Indexes match the queries that exist**, including partial ones for the two hot
  predicates: unread scores, and published assessments per section.
- **Timestamps are `TIMESTAMPTZ`**, not naive `DateTime` — v1 mixes `datetime.utcnow` with
  `func.now()`, which is two different clocks in two different tables.

---

## 6. Scalability notes

- **Caching is explicit and named.** Only three derived values are stored:
  `assessment_stats.*`, `enrollments.final_percent/final_grade`, and (optionally) a
  section headcount. Each is recomputed at one well-defined moment — on save, on publish,
  on enrollment change. Nothing else is denormalised, so there is nothing else to go stale.
- **Reads that grow with class size are bounded.** The student score screen goes from
  O(class size) per view to a single-row read. The teacher course list goes from a full
  scan of the course's scores to a grouped count on an index.
- **Partitioning path, if it is ever needed:** `scores` and `score_audits` partition
  cleanly by term (via `assessment_id` → `section_id` → `term_id`), because a term is
  closed and never rewritten. No other table grows unboundedly.
- **The optional layer is genuinely optional.** `grade_bands`, `notifications`,
  `user_preferences` and `support_tickets` have no inbound FKs from the core, so the
  project can ship without them and add them later without a migration to the core.

### Judgement calls, stated plainly

- **`users.role` is a single column, not a `user_roles` junction table.** Every screen is
  either the student portal or the teacher portal, and a junction table would put a join in
  front of every authorisation check. Nothing except authorisation reads `role`, so if a
  dual-role account (a grad student who TAs) is ever needed, `users.role` can be replaced
  by `user_roles(user_id, role)` without touching another table.
- **`courses` is kept separate from `sections`.** For a small project the two could be one
  table, at the cost of re-storing the title and description for every offering. Keeping
  them apart is what makes the term dropdown and cross-semester history work; collapse them
  only if course reuse across terms is definitively out of scope.
- **Score rows are created lazily**, on first grade entry, and the grade sheet is a LEFT
  JOIN from `enrollments`. Pre-creating a `pending` row per enrollment per assessment is
  the alternative; it makes "Pending" a real row but writes `students × assessments` rows
  per section up front. The LEFT JOIN gets the same screen for less.
- **Weights are not constrained to sum to 100.** That is a cross-row rule; enforcing it in
  the database means a deferred constraint trigger that fires on every grade edit. Validate
  it in the API on assessment save and show a running total in the assignment screen.

---

## 7. Migration path from v1

There is **no migration tooling in the project today** — `fastapi/app/__init__.py:99`
calls `Base.metadata.create_all()`, which creates missing tables and never alters an
existing one. Adding Alembic is step 0; without it, none of this reaches a database that
already has the v1 tables.

1. **Add Alembic**, and baseline it against the current v1 schema.
2. **Create the v2 tables alongside v1** (new names, no collisions except `courses` and
   `scores` — build those as `courses_v2` / `scores_v2` and rename at cutover).
3. **Backfill**, in this order:
   - `terms` — one row for the current semester; every existing course maps to it.
   - `users` ← `auth_users` ⋈ `students` / `teachers`; `role` from which profile row
     exists, `status` = `'active'` where `password IS NOT NULL` else `'invited'`.
   - `student_profiles.student_no` ← `students.student_id`;
     `teacher_profiles` ← `teachers`.
   - `auth_identities` ← `auth_providers` (deduplicate on
     `(provider, provider_user_id)` first — v1 permits duplicates).
   - `courses` ← `DISTINCT (course_id, course_name)` from v1 `courses`;
     `sections` ← v1 `courses` rows, `section_code` from the most common
     `scores.section` in that course, `archived_at` from `is_archive`.
   - `section_instructors` ← v1 `courses.teacher_id`, role `'owner'`.
   - **`enrollments` ← `DISTINCT (course, student)` derived from `scores`.** This is the
     only lossy step: students enrolled but never graded do not exist in v1 and cannot be
     recovered. Re-import the class rosters from CSV after cutover to complete them.
   - `assessments` ← `quizzes` (`kind` defaults to `'assignment'`; `description` and
     `due_at` start NULL); `status` = `'published'` where `is_publish`, `published_at`
     backfilled to `created_at` as an approximation — flag it as such.
   - `scores` ← v1 `scores` joined to the new `enrollments`;
     `viewed_at` = `updated_at` where `unread_flag = false`, else NULL.
   - `score_imports` ← `uploads`, `assessment_id` unrecoverable → attach to the section's
     earliest assessment or leave the history behind and start clean.
4. **Recompute** `assessment_stats` and `enrollments.final_percent` once.
5. **Cut over** the API layer, then drop the v1 tables in a later release — not the same
   one.

Steps 3 and 5 are the only ones that need a maintenance window.

---

## 8. Verification

`schema_v2.sql` was applied to a throwaway `postgres:13-alpine` container (the image in
`docker-compose.yml`) and exercised with seed data. It applies cleanly, and:

**The four things v1 got wrong now come out right**

| Check | Result |
|---|---|
| Grade sheet lists every enrolled student | Alice `92 / graded`, Charlie `-- / pending` — the exact rows in `v1/teacher_edit_score.png` |
| Enrolled headcount | `2`, from `enrollments`, with only one student graded |
| Student dashboard for an ungraded student | `CS101 · Fall 2023 · Turing` appears (v1 showed nothing) |
| "NEW GRADE" badge | resolves through the partial index |

**Constraints reject what v1 accepted**

| # | Attempt | Outcome |
|---|---|---|
| 1 | Score 150 on a 100-mark assessment | rejected by `scores_within_full_mark_trg` |
| 2 | Negative score | rejected by `scores_points_chk` |
| 3 | Second score for the same student + assessment | rejected by `scores_uidx` |
| 4 | Re-adding a score after soft delete | **accepted** — v1 blocked this permanently |
| 5 | Same Google account linked to two users | rejected by `auth_identities_provider_uq` |
| 6 | Score for an enrollment in another section | rejected by `scores_same_section_trg` |
| 7 | Enrolling one student twice in a section | rejected by `enrollments_uq` |
| 8 | Two `owner` instructors on one section | rejected by `section_instructors_owner_uidx` |
| 9 | Deleting a teacher who owns a section | rejected by `ON DELETE RESTRICT` |
| 10 | `status='graded'` with NULL points | rejected by `scores_graded_chk` |
