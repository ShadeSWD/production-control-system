from fastapi import FastAPI
from models import SessionLocal, WorkShift

app = FastAPI()


# Create (Create)
@app.post("/work_shifts/")
async def create_work_shift(closing_status: bool):
    db = SessionLocal()
    db_item = WorkShift(closing_status=closing_status)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/work_shifts/{work_shift_id}")
async def read_item(work_shift_id: int):
    db = SessionLocal()
    work_shift = db.query(WorkShift).filter(WorkShift.id == work_shift_id).first()
    return work_shift
