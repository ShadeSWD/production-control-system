from pydantic import BaseModel
from datetime import date, datetime
from typing import Union


class WorkShiftBase(BaseModel):
    closing_status: bool
    shift_assignment: str
    line: str
    shift: int
    brigade: str
    lot_number: int
    lot_date: date
    nomenclature: str
    ekn_code: str
    rc_identifier: str
    open_at: datetime


class WorkShift(WorkShiftBase):
    id: int
    closed_at: Union[datetime, None]


class WorkShiftCreate(WorkShiftBase):
    closed_at: Union[datetime, None]
