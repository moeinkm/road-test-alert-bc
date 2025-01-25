from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.security import create_access_token
from app.db.session import get_db
from app.crud import crud_user
from app.models import User
from app.models.user import Lead
from app.schemas import Token, UserCreate, UserResponse

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email.is_(str(user_in.email))).first() # todo: get or create new user
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    created_user = crud_user.create_user(db=db, user=user_in)
    lead = db.query(Lead).filter(Lead.email.is_(user_in.email)).first()
    if lead and lead.user_id is None:
        lead.user_id = created_user.id
        db.commit()
        db.refresh(lead)

    return created_user

@router.post("/signin", response_model=Token)
def signin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud_user.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    access_token = create_access_token(data={"sub": user.id})
    return Token(access_token=access_token, token_type="bearer")