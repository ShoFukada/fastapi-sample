from typing import Optional
from sqlalchemy.orm import Session
from app.domain.models.user import User
from app.domain.repositories.user_repository_interface import UserRepositoryInterface
from app.infrastructure.db.models import UserORM

class UserRepository(UserRepositoryInterface):
    def __init__(self):
        self._db: Optional[Session] = None

    def set_db_session(self, db: Session) -> None:
        self._db = db

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        record = self._db.query(UserORM).filter(UserORM.id == user_id).first()
        if not record:
            return None
        return record.to_entity()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        record = self._db.query(UserORM).filter(UserORM.email == email).first()
        if not record:
            return None
        return record.to_entity()

    def create_user(self, user: User):
        new_record = UserORM(
            id = user.id,
            email = user.email,
            display_name = user.display_name,
            hashed_password = user.hashed_password,
        )
        self._db.add(new_record)
        self._db.commit()
        self._db.refresh(new_record)
        return new_record.to_entity()