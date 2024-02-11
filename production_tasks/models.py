from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String

from .datatbase import Base


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


class Product(Base):
    __tablename__ = "products"
    uin = Column(String, primary_key=True, index=True)
    is_aggregated = Column(Boolean, default=False)
    aggregated_at = Column(DateTime, nullable=True)
    lot = Column(Integer, ForeignKey("work_shifts.id", ondelete="CASCADE"))
