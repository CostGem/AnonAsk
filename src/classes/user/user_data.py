from dataclasses import dataclass
from typing import Optional

from src.database.models import UserModel
from src.database.repositories.user import UserRepository


@dataclass
class UserData:
    repository: UserRepository
    user: Optional[UserModel]
