import uuid
from typing import Type, List, Optional

from sqlalchemy.orm import Session

from app.models import User, TestCenter
from app.schemas import UserCreate
from app.core.security import get_password_hash, verify_password


def get_user_by_email(db: Session, email: str) -> Optional[Type[User]]:
    return db.query(User).filter(User.email == email).first()


def get_test_centers(db: Session, center_ids: List[int]) -> List[Type[TestCenter]]:
    return db.query(TestCenter).filter(TestCenter.id.in_(center_ids)).all()


def create_user(db: Session, user: UserCreate):
    db_user = User(
        id=str(uuid.uuid4()),
        email=user.email,
        full_name=user.full_name,
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user