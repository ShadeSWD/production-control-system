import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import (Boolean, Column, Date, DateTime, Integer, String,
                        UniqueConstraint, create_engine, event)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

# Database configurations
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
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
    uid = Column(String, unique=True, index=True)

    __table_args__ = (UniqueConstraint("uid", name="uq_uid"),)


@event.listens_for(WorkShift, "before_insert")
def set_full_name(mapper, connection, target):
    db = SessionLocal()
    target.uid = f"{target.lot_number} {target.lot_date}"
    existing_shift = db.query(WorkShift).filter(WorkShift.uid == target.uid).first()
    if existing_shift:
        db.delete(existing_shift)
        db.commit()
