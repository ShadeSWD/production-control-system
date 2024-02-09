import schemas
from fastapi import FastAPI, HTTPException
from models import Base, Product, SessionLocal, WorkShift, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/work_shifts/", response_model=schemas.WorkShift)
async def create_work_shift(work_shift: schemas.WorkShiftCreate):
    db = SessionLocal()
    existing_work_shift = db.query(WorkShift).filter(WorkShift.lot_number == work_shift.dict()["lot_number"] and
                                                     WorkShift.lot_date == work_shift.dict()["lot_date"]).first()

    if existing_work_shift:
        for key, value in work_shift.dict().items():
            setattr(existing_work_shift, key, value) if value else None
        db.commit()
        db.refresh(existing_work_shift)
        return existing_work_shift

    db_work_shift = WorkShift(**work_shift.dict())
    db.add(db_work_shift)
    db.commit()
    db.refresh(db_work_shift)
    return db_work_shift


@app.post("/products/", response_model=schemas.ProductsList)
async def create_products(products: schemas.ProductsCreate):
    db = SessionLocal()
    products_response = []
    for product in products.root:
        if not db.query(Product).filter(Product.uin == product.dict()["uin"]).first():
            db_product = Product()
            db_product.uin = product.dict()["uin"]
            db_work_shift = (
                db.query(WorkShift).filter(WorkShift.lot_number == product.dict()["lot_number"] and
                                           WorkShift.lot_date == product.dict()["lot_date"]).first()
            )
            if db_work_shift is None:
                continue
            db_product.lot = db_work_shift.id

            db.add(db_product)
            db.commit()
            db.refresh(db_product)

            product_response = db_product
            product_response.lot_number = product.dict()["lot_number"]
            product_response.lot_date = product.dict()["lot_date"]
            products_response.append(product_response)
    return products_response


@app.get("/work_shifts/{work_shift_id}", response_model=schemas.WorkShift)
async def read_work_shift(work_shift_id: int):
    db = SessionLocal()
    db_work_shift = db.query(WorkShift).filter(WorkShift.id == work_shift_id).first()
    if db_work_shift is None:
        raise HTTPException(status_code=404, detail="Shift not found")
    return db_work_shift


@app.patch("/work_shifts/{work_shift_id}", response_model=schemas.WorkShift)
async def update_item(work_shift_id: int, work_shift: schemas.WorkShiftPatch):
    db = SessionLocal()
    db_work_shift = db.query(WorkShift).filter(WorkShift.id == work_shift_id).first()

    if db_work_shift is None:
        raise HTTPException(status_code=404, detail="Shift not found")

    for key, value in work_shift.dict().items():
        setattr(db_work_shift, key, value) if value else None

    db.commit()
    db.refresh(db_work_shift)
    return db_work_shift
