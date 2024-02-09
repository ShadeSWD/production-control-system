from datetime import date, datetime
from typing import Union, Optional

from pydantic import BaseModel, Field


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
    closing_status: bool = Field(validation_alias="СтатусЗакрытия")
    shift_assignment: str = Field(validation_alias="ПредставлениеЗаданияНаСмену")
    line: str = Field(validation_alias="РабочийЦентр")
    shift: int = Field(validation_alias="Смена")
    brigade: str = Field(validation_alias="Бригада")
    lot_number: int = Field(validation_alias="НомерПартии")
    lot_date: date = Field(validation_alias="ДатаПартии")
    nomenclature: str = Field(validation_alias="Номенклатура")
    ekn_code: str = Field(validation_alias="КодЕКН")
    rc_identifier: str = Field(validation_alias="ИдентификаторРЦ")
    open_at: datetime = Field(validation_alias="ДатаВремяНачалаСмены")
    closed_at: Union[datetime, None] = Field(validation_alias="ДатаВремяОкончанияСмены")


class WorkShiftPatch(WorkShiftBase):
    closing_status: Optional[bool] = None
    shift_assignment: Optional[str] = None
    line: Optional[str] = None
    shift: Optional[int] = None
    brigade: Optional[str] = None
    lot_number: Optional[int] = None
    lot_date: Optional[date] = None
    nomenclature: Optional[str] = None
    ekn_code: Optional[str] = None
    rc_identifier: Optional[str] = None
    open_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
