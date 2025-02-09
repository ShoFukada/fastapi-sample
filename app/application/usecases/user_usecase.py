from typing import List, Optional
from app.domain.models.user import User
from app.domain.repositories.user_repository_interface import UserRepositoryInterface
from injector import inject
from app.core.auth import get_password_hash, verify_password

class UserUseCase:
    @inject
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository
    
    def create_user(self, email: str, display_name: str, password: str) -> User:
        # FIXME usecase層にこれ置くの正しい？
        hashed_password = get_password_hash(password)
        new_user = User(
            id=0,
            email=email,
            display_name=display_name,
            hashed_password=hashed_password
        )
        return self.user_repository.create_user(new_user)
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.user_repository.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.user_repository.get_user_by_id(user_id)