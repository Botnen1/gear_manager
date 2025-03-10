import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'data', 'gear.db')}"

def get_session():
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    Session = sessionmaker(bind=engine)
    return Session()
