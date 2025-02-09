
from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models.user import User

class UserRepositoryInterface(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        raise NotImplementedError
    
    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError
    
    @abstractmethod
    def create_user(self, user: User) -> User:
        raise NotImplementedError