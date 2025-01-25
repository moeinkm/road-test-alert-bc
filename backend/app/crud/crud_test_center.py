from typing import List, Type

from sqlalchemy.orm import Session

from app.schemas import TestCenterCreate
from app.models.test_center import TestCenter


def get_test_centers_by_ids(db: Session, center_ids: List[int]) -> list[Type[TestCenter]]:
    """
    Retrieve test centers by their IDs.

    :param center_ids: List of test center IDs
    :param db: Database session
    :return: List of TestCenter objects
    """
    return db.query(TestCenter).filter(TestCenter.id.in_(center_ids)).all()

def create_test_center(db: Session, test_center: TestCenterCreate) -> TestCenter:
    db_test_center = TestCenter(**test_center.dict())
    db.add(db_test_center)
    db.commit()
    db.refresh(db_test_center)
    return db_test_center