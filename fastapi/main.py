import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import fastapi_app
from app.db import Base, engine
from app import models

Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware
app = fastapi_app

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "https://25cs212g12repo-mauve.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)