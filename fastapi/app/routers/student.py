#!/usr/bin/env python3
# fastapi/app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import distinct
from app.db import get_db
from app.models import Student, Score, Quiz, Course
from app.routers.auth import get_cerrent_user
from app.models.authuser import AuthUser

router = APIRouter(
    prefix="/student",
    tags=["Student"]
)

def  