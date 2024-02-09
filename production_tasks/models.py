import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy import (Boolean, Column, Date, DateTime, ForeignKey, Integer,
                        String, create_engine, event)
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
    shift_start = Column(DateTime)
    shift_end = Column(DateTime)
    closed_at = Column(DateTime, nullable=True)


def check_unique_lot(target):
    db = SessionLocal()
    existing_shifts = (
        db.query(WorkShift)
        .filter(
            WorkShift.lot_number == target.lot_number,
            WorkShift.lot_date == target.lot_date,
            WorkShift.id != target.id,
        )
        .first()
    )
    if existing_shifts:
        raise HTTPException(status_code=422, detail="Shift already exists")


@event.listens_for(WorkShift, "before_insert")
def check_lot_insert(mapper, connection, target):
    check_unique_lot(target)


@event.listens_for(WorkShift, "before_update")
def check_lot_update(mapper, connection, target):
    check_unique_lot(target)


class Product(Base):
    __tablename__ = "products"
    uin = Column(String, primary_key=True, index=True)
    is_aggregated = Column(Boolean, default=False)
    aggregated_at = Column(DateTime, nullable=True)
    lot = Column(Integer, ForeignKey("work_shifts.id", ondelete="CASCADE"))
