from fastapi import FastAPI, HTTPException
from models import SessionLocal, WorkShift, Base, engine
from datetime import date, datetime

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/work_shifts/")
async def create_work_shift(closing_status: bool,
                            shift_assignment: str,
                            line: str,
                            shift: int,
                            brigade: str,
                            lot_number: int,
                            lot_date: date,
                            nomenclature: str,
                            ekn_code: str,
                            rc_identifier: str,
                            open_at: datetime,
                            closed_at: datetime | None):
    db = SessionLocal()
    db_item = WorkShift(closing_status=closing_status,
                        shift_assignment=shift_assignment,
                        line=line,
                        shift=shift,
                        brigade=brigade,
                        lot_number=lot_number,
                        lot_date=lot_date,
                        nomenclature=nomenclature,
                        ekn_code=ekn_code,
                        rc_identifier=rc_identifier,
                        open_at=open_at,
                        closed_at=closed_at)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/work_shifts/{work_shift_id}")
async def read_item(work_shift_id: int):
    db = SessionLocal()
    work_shift = db.query(WorkShift).filter(WorkShift.id == work_shift_id).first()
    if work_shift is None:
        raise HTTPException(status_code=404, detail="Shift not found")
    return work_shift
