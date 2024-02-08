from fastapi import FastAPI, HTTPException
from models import SessionLocal, WorkShift, Base, engine
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/work_shifts/", response_model=schemas.WorkShift)
async def create_work_shift(work_shift: schemas.WorkShiftCreate):
    db = SessionLocal()
    db_work_shift = WorkShift(**work_shift.dict())
    db.add(db_work_shift)
    db.commit()
    db.refresh(db_work_shift)
    return db_work_shift


@app.get("/work_shifts/{work_shift_id}", response_model=schemas.WorkShift)
async def read_work_shift(work_shift_id: int):
    db = SessionLocal()
    db_work_shift = db.query(WorkShift).filter(WorkShift.id == work_shift_id).first()
    if db_work_shift is None:
        raise HTTPException(status_code=404, detail="Shift not found")
    return db_work_shift


@app.patch("/work_shifts/{work_shift_id}", response_model=schemas.WorkShift)
async def update_item(work_shift_id: int, work_shift: schemas.WorkShiftBase):
    db = SessionLocal()
    db_work_shift = db.query(WorkShift).filter(WorkShift.id == work_shift_id).first()

    if work_shift is None:
        raise HTTPException(status_code=404, detail="Shift not found")

    for key, value in work_shift.dict().items():
        setattr(db_work_shift, key, value) if value else None

    db.commit()
    db.refresh(db_work_shift)
    return db_work_shift
