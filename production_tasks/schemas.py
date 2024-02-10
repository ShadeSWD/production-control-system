from datetime import date, datetime
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, RootModel


class Pagination(BaseModel):
    page: int
    size: int
    total: int


class ProductBase(BaseModel):
    uin: str


class ProductCreate(ProductBase):
    uin: str = Field(validation_alias="УникальныйКодПродукта")
    lot_number: int = Field(validation_alias="НомерПартии")
    lot_date: date = Field(validation_alias="ДатаПартии")


class Product(ProductBase):
    is_aggregated: bool
    aggregated_at: Union[datetime, None]
    lot: int


class ProductsCreate(RootModel):
    root: List[ProductCreate]


class ProductsList(RootModel):
    root: List[Product]


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
    shift_start: datetime


class WorkShift(WorkShiftBase):
    id: int
    closed_at: Optional[datetime] = None


class WorkShiftProducts(WorkShift):
    products: list


class WorkShiftList(BaseModel):
    work_shifts: List[WorkShift]
    pagination: Pagination


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
    shift_start: datetime = Field(validation_alias="ДатаВремяНачалаСмены")
    shift_end: datetime = Field(validation_alias="ДатаВремяОкончанияСмены")


class WorkShiftPatch(WorkShiftBase):
    closing_status: Optional[bool] = None
    shift_assignment: Optional[str] = None
    line: Optional[str] = None
    shift: Optional[int] = None
    brigade: Optional[str] = None
    nomenclature: Optional[str] = None
    ekn_code: Optional[str] = None
    rc_identifier: Optional[str] = None
