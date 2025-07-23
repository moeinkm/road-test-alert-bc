from typing import List

from sqlalchemy.orm import Session

from app.models.center import Center


def get_centers_by_ids(db: Session, center_ids: List[int]) -> List[Center]:
    """
    Retrieve test centers by their IDs.

    :param center_ids: List of test center IDs
    :param db: Database session
    :return: List of Center objects
    """
    return db.query(Center).filter(Center.id.in_(center_ids)).all()
