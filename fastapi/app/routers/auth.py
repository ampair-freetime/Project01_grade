#!/usr/bin/env python3
# fastapi/app/routers/auth.py

import logging
import secrets
from fastapi import APIRouter, Request, Depends, HTTPException, status, Response
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.auth import UserResponse, Message, UserLogin, UserSignin
from pwdlib import PasswordHash

from app.models.authuser import AuthUser
from app.models.authprovider import AuthProvider
from app.models.teacher import Teacher
from app.models.student import Student
from app.config import settings
from jose import jwt, JWTError
from datetime import datetime, timedelta
from httpx import AsyncClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set this logger to DEBUG

router = APIRouter()

# JWT Configuration
SECRET_KEY = settings.jwt_secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 1 day (1440 minutes)

# Google OAuth Configuration
GOOGLE_CLIENT_ID = settings.google_client_id or "your-google-client-id"
GOOGLE_CLIENT_SECRET = settings.google_client_secret or "your-google-client-secret"
GOOGLE_REDIRECT_URI = "http://localhost:8080/auth/google/auth"  # Adjust as needed
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

password_hash = PasswordHash.recommended()


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    csrf_token = secrets.token_hex(16)
    to_encode["csrf_token"] = csrf_token
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")


async def get_current_user(request: Request, db: Session = Depends(get_db)):
    logger.debug(f"Checking JWT cookie in get_current_user")
    token = request.cookies.get("jwt")
    logger.debug(f"JWT cookie: {token}")
    if not token:
        logger.error("Missing JWT cookie in get_current_user")
        raise HTTPException(status_code=401, detail="Missing JWT cookie")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"JWT payload: {payload}")
        user_id: str = payload.get("sub")
        logger.debug(f"Extracted user_id from sub: {user_id}")
        if user_id is None:
            logger.error("Invalid token: subject missing")
            raise HTTPException(
                status_code=401, detail="Invalid token: subject missing")
        user = db.query(AuthUser).filter(AuthUser.auth_user_id == int(user_id)).first()
        if user is None:
            logger.error(f"User not found for id: {user_id}")
            raise HTTPException(status_code=401, detail="User not found")
        logger.debug(f"User found: {user.email}")
        return user
    except JWTError as e:
        logger.error(f"JWT decoding failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/", response_model=Message)
async def hello():
    """
    **Root Auth Endpoint**

    Returns a simple greeting message to verify the auth router is active.
    """
    logger.info("Auth hello endpoint accessed")
    return {"message": "From auth.py: Hello World!"}


@router.get("/login_with_google", response_description="Redirects to Google OAuth")
async def login(request: Request):
    """
    **Initiate Google OAuth Login**

    Constructs the Google OAuth URL with identifying scopes (openid, email, profile)
    and redirects the user to Google's consent page.
    """
    # ... implementation details ...
    redirect_uri = str(request.url_for("google_auth"))
    auth_url = (
        f"{GOOGLE_AUTH_URL}?response_type=code&client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={redirect_uri}&scope=openid%20email%20profile"
    )
    logger.info("Redirecting to Google OAuth")
    return RedirectResponse(url=auth_url)


@router.get("/google/auth", name="google_auth", response_description="Redirects to Frontend with JWT")
async def google_auth(request: Request, db: Session = Depends(get_db)):
    """
    **Google OAuth Callback**

    Handles the callback from Google:
    1. Exchanges the authorization code for an access token.
    2. Fetches user profile information from Google.
    3. Creates or updates the user in the local database.
    4. Generates a valid JWT for the session.
    5. Redirects the user back to the frontend with the JWT query parameter.
    """
    # ... implementation details ...
    try:
        code = request.query_params.get("code")
    # ... rest of the function ...
        # (This is a large block, I will strictly follow replacement rules in next step, 
        # simplifying here for the thought process)
        if not code:
            raise ValueError("No authorization code provided")

        async with AsyncClient() as client:
            token_response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "code": code,
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "redirect_uri": str(request.url_for("google_auth")),
                    "grant_type": "authorization_code",
                },
            )
            token_data = token_response.json()
            if "error" in token_data:
                raise ValueError(f"Google OAuth error: {token_data['error']}")
            access_token = token_data.get("access_token")

            user_info_response = await client.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            user_info = user_info_response.json()
            logger.debug(f"Google profile: {user_info}")

        # new_provider = AuthProvider(
                # auth_user_id= current_user.auth_user_id,
                # email_provider = user_info["email"]
                # provider="google",
                # provider_user_id=user_info["id"]
            # )


        provider = db.query(AuthProvider).filter(
            AuthProvider.provider == "google",
            AuthProvider.provider_user_id == user_info["id"]
        ).first()

        if provider:
            user = db.query(AuthUser).filter(
                AuthUser.auth_user_id == provider.auth_user_id
            ).first()
        else:
            user = db.query(AuthUser).filter(
                AuthUser.email == user_info["email"]
            ).first()

            # if not user:
            #     user = AuthUser(email=user_info["email"])
            #     db.add(user)
            #     db.commit()
            #     db.refresh(user)

            # new_provider = AuthProvider(
            #     auth_user_id=user.auth_user_id,
            #     provider="google",
            #     provider_user_id=user_info["id"]
            # )

            # db.add(new_provider)
            # db.commit()

        jwt_token = create_access_token(
            data={
                "sub": str(user.auth_user_id),
                "email": user.email
            },
            expires_delta=timedelta(days=1)
        )

        frontend_url = settings.frontend_login_success_uri
        logger.info(f"Redirecting to frontend with token for {user.email}")
        return RedirectResponse(url=f"{frontend_url}?token={jwt_token}")

    except Exception as e:
        logger.error(f"Error processing Google auth callback: {e}")
        return RedirectResponse(url=settings.frontend_login_failure_uri)

@router.post("/login")
async def login(login_data: UserLogin,response: Response, db: Session = Depends(get_db)):
    # ไม่ต้อง ตรวจ . หรือ _ เพราะเสริชหาข้อมูลจาก data base ได้เลย
    user = db.query(AuthUser).filter(AuthUser.email == login_data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Email Not Found")
    if user.password is None:
        raise HTTPException(status_code=401, detail="Your are not sign up")
    if not password_hash.verify(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Password Not Correct")
    #สร้าง ข้อมูลเพื่อทำ JWT Token
    user_role = "student" if user.student else "teacher"
    payload = {
        "sub": str(user.auth_user_id),
        "user_role": user_role
    }
    jwt_token = create_access_token(payload, expires_delta=timedelta(days=1))

    decoded = jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])
    csrf_token = decoded.get("csrf_token")
    #บันทึก jwt ลง cookie
    response.set_cookie(
        key="jwt",
        value=jwt_token,
        httponly=True,
        secure=settings.jwt_cookie_secure,
        samesite=settings.jwt_cookie_samesite
    )
    return {
        "message": "Login successful",
        "csrf_token": csrf_token,
        "role": user_role
    }

@router.post("/register")
async def register(signin_data: UserSignin, db: Session = Depends(get_db)):
    #check email is teacher or student
    #example email stu_dent@cmu.ac.th นักเรียนต้องมี ขีดเท่านั้น tea.cher@cmu.ac.th teacher จะเป็นจุดก่อนเสมอ
    #student
    if signin_data.student_id:
        user = db.query(AuthUser).filter(AuthUser.email == signin_data.email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Yor are not invited")
        #this user not rewrite 2 ขั้น ใช้ password เป็น none และ student_id เทียบกัน
        avatar = f"https://ui-avatars.com/api/?name={signin_data.first_name}&size=128&background=random"
        if user.student.student_id != signin_data.student_id:
            raise HTTPException(status_code=401, detail="ID not match please enter new ID")
        if user.student and user.password is None:
            user.student.first_name = signin_data.first_name
            user.student.last_name = signin_data.last_name
            user.student.middle_name = signin_data.middle_name
            user.password = password_hash.hash(signin_data.password)
            user.student.avatar_url = avatar
            db.commit()
            return {"message": "Account successful"}
        else:
            raise HTTPException(status_code=401, detail="This user already used")
    else:
        #teacher
        user = db.query(AuthUser).filter(AuthUser.email == signin_data.email).first()
        if user:
            raise HTTPException(status_code=401, detail="Email already used")
            #ต้องไม่มี ใน databse
        new_auth = AuthUser(
            email=signin_data.email,
            password=password_hash.hash(signin_data.password)
        )
        db.add(new_auth)
        db.commit()
        db.refresh(new_auth)

        avatar = f"https://ui-avatars.com/api/?name={signin_data.first_name}&size=128&background=random"
        new_profile = Teacher(
            first_name=signin_data.first_name,
            last_name= signin_data.last_name,
            middle_name= signin_data.middle_name,
            auth_user_id=new_auth.auth_user_id,
            avatar_url=avatar,
        )
        db.add(new_profile)
        db.commit()
    #if request.email แยก เป็น 
    #ใช้สมัครสำหรับ นักเรียนใหม่ เพื่อเข้าสู่ระบบ เช็ค database แล้วเปลี่ยนเอา หรือ สร้าง database ใหม่
    #ถ้ามีเวลาให้เอาอันนี้ออก แล้ว ใช้ การ ส่งรหัสผ่าน email (advance)
    return {"message": "Sign up completed"}

@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie(
        key="jwt",
        path="/",
        httponly=True,
        samesite=settings.jwt_cookie_samesite,
        secure=settings.jwt_cookie_secure
    )
    """
    **Logout User**
    Instructs the client to clear the JWT token.
    Note: Real server-side logout would require a token blacklist.
    """
    logger.info("User logged out")
    return {"message": "Logout successful"}


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: AuthUser = Depends(get_current_user)):
    """
    **Get Current User Profile**

    Returns the profile information of the currently authenticated user.
    Requires a valid JWT token in the `jwt` cookie or Authorization header (logic depends on `get_current_user`).
    """
    logger.info(f"Fetching profile for {current_user.email}")
    if current_user.student:
        return {"id": current_user.auth_user_id,
                "email": current_user.email, 
                "first_name": current_user.student.first_name,
                "middle_name": current_user.student.middle_name,
                "last_name": current_user.student.last_name,
                "avatar_url": current_user.student.avatar_url,
                "student_id": current_user.student.student_id}
    else:
        return {"id": current_user.auth_user_id,
                "email": current_user.email, 
                "first_name": current_user.teacher.first_name,
                "middle_name": current_user.teacher.middle_name,
                "last_name": current_user.teacher.last_name,
                "avatar_url": current_user.teacher.avatar_url}

def register_routes(router_instance: APIRouter):
    router_instance.include_router(router)