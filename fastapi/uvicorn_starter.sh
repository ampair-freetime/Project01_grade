#!/bin/sh
# Ensure Python uses the correct path
export PATH="/usr/local/bin:$PATH"

# Debug: Verify if Python sees Uvicorn
python3 -m uvicorn --help >/dev/null 2>&1 || { echo "Error: uvicorn not found"; exit 1; }

if [ "$APP_ENV" = "development" ]; then

    # Check if we are using Supabase (skip local DB wait)
    if [ "$USE_SUPABASE" != "true" ]; then
        echo -n "Waiting for the DBMS to accept connection "
        while [ 1 ]; do
            if nc -vz db "$DATABASE_PORT"; then
                break
            fi
            echo -n "."
            sleep 1
        done
        echo ""
    else
        echo "Using Supabase - Skipping local DB wait..."
    fi

    # โปรเจกต์ไม่มี alembic.ini/versions — ใช้ script ที่รันซ้ำได้แทน
    # (สร้างตารางที่ขาด + enrollments + join_code + backfill)
    # port เปิดแล้วแต่ Postgres อาจยังไม่พร้อมตอนบูตครั้งแรก — ลองซ้ำ
    echo "Running database migrations..."
    tries=0
    until python3 migrate_enrollment.py; do
        tries=$((tries + 1))
        if [ "$tries" -ge 10 ]; then
            echo "Error: migrations failed"
            exit 1
        fi
        echo "Migration failed, retrying ($tries/10)..."
        sleep 3
    done
    echo "Migrations applied"

    if [ "$DEBUG" = "1" ]; then
        echo "Running FastAPI in Development Mode (with auto-reload)"
        python3 -m uvicorn main:fastapi_app --host 0.0.0.0 --port 8080 --reload  # Runs like Flask dev server
    else
        echo "Starting FastAPI in development mode with Gunicorn (managing Uvicorn workers)"
        python3 -m gunicorn -c "$PWD"/gunicorn.config.py main:fastapi_app
    fi
else
    echo "Starting FastAPI in production mode with Gunicorn"
    python3 -m gunicorn -c "$PWD"/gunicorn.config.py main:fastapi_app
fi
exec "$@"
