from sqlalchemy import create_engine
import os
from app.core.config import DATABASE_URL
from app.db.base import Base

engine = create_engine(DATABASE_URL,echo=True)

Base.metadata.create_all(engine)
