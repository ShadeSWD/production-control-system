from datetime import datetime
from typing import Optional, List

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field, field_validator

from models import WorkShift


class WorkShiftFilter(Filter):
    order_by: Optional[list[str]]
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

    @field_validator("order_by")
    def restrict_sortable_fields(cls, value):
        if value is None:
            return None

        allowed_field_names = ["lot_date", "lot_number", "shift_start", "shift_end", "closed_at"]

        for field_name in value:
            field_name = field_name.replace("+", "").replace("-", "")  #
            if field_name not in allowed_field_names:
                raise ValueError(f"You may only sort by: {', '.join(allowed_field_names)}")

        return value
