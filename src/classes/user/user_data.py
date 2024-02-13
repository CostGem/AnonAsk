from dataclasses import dataclass
from typing import Optional

from src.database.models import UserModel, LocaleModel
from src.database.repositories import UserRepository


@dataclass
class UserData:
    repository: UserRepository
    user: Optional[UserModel]
    locale: Optional[LocaleModel]
