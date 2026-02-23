import os

DATABASE_URL = os.getenv("DATABASE_URL","postgresql+psycopg2://postgres:admin123@localhost:5432/police_servillience")