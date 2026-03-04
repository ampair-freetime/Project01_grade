import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import fastapi_app
from app.db import Base, engine
from app import models


Base.metadata.create_all(bind=engine)

app = fastapi_app
