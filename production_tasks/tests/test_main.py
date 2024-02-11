from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy_utils import drop_database

from ..datatbase import Base
from ..main import app, get_db

TEST_SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


def test_create_work_shift():
    response = client.post(
        "/work_shifts/",
        json={
            "СтатусЗакрытия": "false",
            "ПредставлениеЗаданияНаСмену": "string",
            "РабочийЦентр": "string",
            "Смена": 0,
            "Бригада": "string",
            "НомерПартии": 0,
            "ДатаПартии": "2024-02-11",
            "Номенклатура": "string",
            "КодЕКН": "string",
            "ИдентификаторРЦ": "string",
            "ДатаВремяНачалаСмены": "2024-02-11T12:13:18.228Z",
            "ДатаВремяОкончанияСмены": "2024-02-11T12:13:18.228Z",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "brigade": "string",
        "closed_at": None,
        "closing_status": False,
        "ekn_code": "string",
        "id": 1,
        "line": "string",
        "lot_date": "2024-02-11",
        "lot_number": 0,
        "nomenclature": "string",
        "rc_identifier": "string",
        "shift": 0,
        "shift_assignment": "string",
        "shift_end": "2024-02-11T12:13:18.228000",
        "shift_start": "2024-02-11T12:13:18.228000",
    }
