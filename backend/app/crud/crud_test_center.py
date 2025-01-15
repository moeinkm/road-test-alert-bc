from typing import List, Type
from sqlalchemy.orm import Session
from app.models.test_center import TestCenter
from app.schemas.test_center import TestCenterCreate

def get_test_centers(db: Session) -> List[Type[TestCenter]]:
    return db.query(TestCenter).all()

def create_test_center(db: Session, test_center: TestCenterCreate) -> TestCenter:
    db_test_center = TestCenter(**test_center.dict())
    db.add(db_test_center)
    db.commit()
    db.refresh(db_test_center)
    return db_test_center