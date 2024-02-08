from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

# Database configurations
SQLALCHEMY_DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:" \
                          f"{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class WorkShift(Base):
    __tablename__ = "work_shifts"
    id = Column(Integer, primary_key=True, index=True)
    closing_status = Column(Boolean)
    shift_assignment = Column(String)
    line = Column(String)
    shift = Column(Integer)
    brigade = Column(String)
    lot_number = Column(Integer, index=True)
    lot_date = Column(Date, index=True)
    nomenclature = Column(String)
    ekn_code = Column(String)
    rc_identifier = Column(String)
    open_at = Column(DateTime)
    closed_at = Column(DateTime, nullable=True)
