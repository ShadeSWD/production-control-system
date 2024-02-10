from datetime import datetime
from typing import Optional, List

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from models import WorkShift


class WorkShiftFilter(Filter):
    closing_status: Optional[bool] = None
    lot_number: Optional[int] = None
    shift_assignment__like: Optional[str] = Field(default=None, alias="assignment_like")
    lot_date__gte: Optional[datetime] = Field(default=None, alias="lot_date_after")
    lot_date__lte: Optional[datetime] = Field(default=None, alias="lot_date_before")
    shift_start__gte: Optional[datetime] = Field(default=None, alias="start_after")
    shift_start__lte: Optional[datetime] = Field(default=None, alias="start_before")
    shift_end__gte: Optional[datetime] = Field(default=None, alias="end_after")
    shift_end__lte: Optional[datetime] = Field(default=None, alias="end_before")

    class Constants(Filter.Constants):
        model = WorkShift

    class Config:
        extra = "allow"
