from dataclasses import dataclass
from typing import Optional

from src.database.models import UserModel, RoleModel, StatusModel
from src.database.repositories import UserRepository


@dataclass
class UserData:
    repository: UserRepository
    user: Optional[UserModel]
    role: Optional[RoleModel]
    status: Optional[StatusModel]
