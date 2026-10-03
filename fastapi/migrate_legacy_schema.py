"""Upgrade the original integer-ID schema without deleting existing rows.

Called before creating enrollments. Stop application workers before migration.
Column renames, ID casts, and foreign-key restoration share one transaction.
"""

from sqlalchemy import Integer, inspect, text


# Parent IDs and every corresponding foreign key must be converted together.
TEXT_IDS = {
    "auth_users": ("auth_user_id",),
    "auth_providers": ("provider_id", "auth_user_id"),
    "students": ("student_id", "auth_user_id"),
    "teachers": ("teacher_id", "auth_user_id"),
    "courses": ("teacher_id",),
    "quizzes": ("quiz_id",),
    "scores": ("score_id", "quiz_id", "student_id"),
    "uploads": ("upload_id", "teacher_id"),
    "enrollments": ("enrollment_id", "student_id"),
}
UUID_IDS = {
    ("auth_users", "auth_user_id"),
    ("auth_providers", "provider_id"),
    ("teachers", "teacher_id"),
    ("quizzes", "quiz_id"),
    ("scores", "score_id"),
    ("uploads", "upload_id"),
    ("enrollments", "enrollment_id"),
}


def migrate_legacy_schema(engine):
    with engine.begin() as conn:
        tables = set(inspect(conn).get_table_names(schema="public"))
        for table in ("courses", "quizzes", "uploads"):
            if table not in tables:
                continue
            columns = {c["name"]: c for c in inspect(conn).get_columns(table, schema="public")}
            # The old course_id was the internal integer PK/FK. The new
            # courses.course_id is a separate, optional human-facing code.
            if ("course_code" not in columns and "course_id" in columns
                    and isinstance(columns["course_id"]["type"], Integer)):
                conn.execute(text(f'ALTER TABLE public."{table}" RENAME COLUMN course_id TO course_code'))

        conversions = []
        for table, names in TEXT_IDS.items():
            if table not in tables:
                continue
            columns = {c["name"]: c for c in inspect(conn).get_columns(table, schema="public")}
            conversions.extend(
                (table, name) for name in names
                if name in columns and isinstance(columns[name]["type"], Integer)
            )

        if conversions:
            # Save actual definitions so ON DELETE/UPDATE and deferrability
            # survive. Renaming above has already updated referenced columns.
            constraints = conn.execute(text("""
                SELECT n.nspname AS schema_name, t.relname AS table_name,
                       c.conname, pg_get_constraintdef(c.oid) AS definition
                FROM pg_constraint c
                JOIN pg_class t ON t.oid = c.conrelid
                JOIN pg_namespace n ON n.oid = t.relnamespace
                WHERE c.contype = 'f' AND (
                    c.conrelid IN (SELECT oid FROM pg_class
                        WHERE relnamespace = 'public'::regnamespace)
                    OR c.confrelid IN (SELECT oid FROM pg_class
                        WHERE relnamespace = 'public'::regnamespace)
                )
            """)).mappings().all()
            quote = conn.dialect.identifier_preparer.quote
            for fk in constraints:
                table = f'{quote(fk["schema_name"])}.{quote(fk["table_name"])}'
                conn.execute(text(f'ALTER TABLE {table} DROP CONSTRAINT {quote(fk["conname"])}'))
            for table, name in conversions:
                column = f'public."{table}" ALTER COLUMN "{name}"'
                conn.execute(text(f'ALTER TABLE {column} DROP DEFAULT'))
                conn.execute(text(f'ALTER TABLE {column} TYPE VARCHAR USING "{name}"::text'))
                if (table, name) in UUID_IDS:
                    conn.execute(text(f'ALTER TABLE {column} SET DEFAULT gen_random_uuid()'))
            for fk in constraints:
                table = f'{quote(fk["schema_name"])}.{quote(fk["table_name"])}'
                conn.execute(text(
                    f'ALTER TABLE {table} ADD CONSTRAINT {quote(fk["conname"])} {fk["definition"]}'
                ))

        if "courses" in tables:
            conn.execute(text('ALTER TABLE public.courses ADD COLUMN IF NOT EXISTS course_id VARCHAR'))
        if "quizzes" in tables:
            conn.execute(text('ALTER TABLE public.quizzes ADD COLUMN IF NOT EXISTS is_publish BOOLEAN DEFAULT FALSE'))
        print(f"Legacy schema ready; converted {len(conversions)} ID columns")
