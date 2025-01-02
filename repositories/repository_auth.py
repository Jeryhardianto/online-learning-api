from sqlalchemy.orm import Session
from models.model_user import User
from schemas.user_schema import UserCreate
class UserRepositories:
    def __init__(self, session: Session):
        self.session = session

    def get_user(self, user_id: int):
        return self.session.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str):
        return self.session.query(User).filter(User.email == email).first()

    def get_users(self, skip: int = 0, limit: int = 100):
        return self.session.query(User).offset(skip).limit(limit).all()

    def store_user(self, data: UserCreate):
        db_user = User(fullname=data.fullname, email=data.email, password=data.password)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user
