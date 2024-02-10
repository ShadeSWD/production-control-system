import datetime
import math

import schemas
from fastapi import FastAPI, HTTPException, Query
from fastapi_filter import FilterDepends
from filters import WorkShiftFilter
from models import Base, Product, SessionLocal, WorkShift, engine
from sqlalchemy import select

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/work_shifts/", response_model=schemas.WorkShift)
async def create_work_shift(work_shift: schemas.WorkShiftCreate):
    db = SessionLocal()
    existing_work_shift = (
        db.query(WorkShift)
        .filter(
            WorkShift.lot_number == work_shift.dict()["lot_number"],
            WorkShift.lot_date == work_shift.dict()["lot_date"],
        )
        .first()
    )

    if existing_work_shift:
        existing_work_shift = update_work_shift(existing_work_shift, work_shift)
        db.commit()
        db.refresh(existing_work_shift)
        return existing_work_shift

    db_work_shift = WorkShift(**work_shift.dict())
    if db_work_shift.closing_status:
        if (
            db_work_shift.shift_end
            > datetime.datetime.now(datetime.UTC)
            > db_work_shift.shift_start
        ):
            db_work_shift.closed_at = datetime.datetime.now(datetime.UTC)
        else:
            db_work_shift.closed_at = db_work_shift.shift_end
    db.add(db_work_shift)
    db.commit()
    db.refresh(db_work_shift)
    return db_work_shift


@app.post("/products/", response_model=schemas.ProductsList)
async def create_products(products: schemas.ProductsCreate):
    db = SessionLocal()
    products_response = []
    for product in products.root:
        if not db.query(Product).get(product.dict()["uin"]):
            db_product = Product()
            db_product.uin = product.dict()["uin"]
            db_work_shift = (
                db.query(WorkShift)
                .filter(
                    WorkShift.lot_number == product.dict()["lot_number"]
                    and WorkShift.lot_date == product.dict()["lot_date"]
                )
                .first()
            )
            if db_work_shift is None:
                continue
            db_product.lot = db_work_shift.id

            db.add(db_product)
            db.commit()
            db.refresh(db_product)

            products_response.append(db_product)
    return products_response


@app.get("/work_shifts", response_model=schemas.WorkShiftList)
async def get_work_shifts(
    work_shift_filter: WorkShiftFilter = FilterDepends(WorkShiftFilter),
    page: int = Query(ge=0, default=0),
    size: int = Query(ge=1, le=100, default=100),
):
    db = SessionLocal()
    query = select(WorkShift)
    query = work_shift_filter.filter(query)
    query = work_shift_filter.sort(query)
    result = db.execute(query)

    offset = page * size
    limit = (page + 1) * size
    response = result.scalars().all()
    response = {
        "work_shifts": response[offset:limit],
        "pagination": {
            "page": page,
            "size": size,
            "total": math.ceil(len(response) / size) - 1,
        },
    }
    return response


@app.get("/work_shifts/{work_shift_id}", response_model=schemas.WorkShiftProducts)
async def read_work_shift(work_shift_id: int):
    db = SessionLocal()
    db_work_shift = db.query(WorkShift).get(work_shift_id)
    if db_work_shift is None:
        raise HTTPException(status_code=404, detail="Shift not found")

    products = [
        product.uin
        for product in db.query(Product).filter(Product.lot == db_work_shift.id)
    ]
    db_work_shift.products = products
    return db_work_shift


@app.patch("/work_shifts/{work_shift_id}", response_model=schemas.WorkShift)
async def patch_work_shift(work_shift_id: int, work_shift: schemas.WorkShiftPatch):
    db = SessionLocal()
    db_work_shift = db.query(WorkShift).get(work_shift_id)

    if db_work_shift is None:
        raise HTTPException(status_code=404, detail="Shift not found")

    db_work_shift = update_work_shift(db_work_shift, work_shift)

    db.commit()
    db.refresh(db_work_shift)
    return db_work_shift


@app.post("/aggregate/{work_shift_id}/{product_uin}")
async def aggregate_product(work_shift_id: int, product_uin: str):
    db = SessionLocal()

    product = db.query(Product).get(product_uin)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.is_aggregated:
        raise HTTPException(
            status_code=400,
            detail=f"unique code already used at {product.aggregated_at}",
        )

    if product.lot != work_shift_id:
        raise HTTPException(
            status_code=400, detail=f"unique code is attached to another batch"
        )

    product.is_aggregated = True
    product.aggregated_at = datetime.datetime.now(datetime.UTC)
    db.commit()

    return {"uin": product.uin}


def update_work_shift(work_shift, data):
    now_closed = work_shift.closing_status

    for key, value in data.dict().items():
        setattr(work_shift, key, value) if value else None
    work_shift.closing_status = data.dict()["closing_status"]

    if not now_closed and work_shift.closing_status and not work_shift.closed_at:
        work_shift.closed_at = datetime.datetime.now(datetime.UTC)

    if not work_shift.closing_status:
        work_shift.closed_at = None

    return work_shift
