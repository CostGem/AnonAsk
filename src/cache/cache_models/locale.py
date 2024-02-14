from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin


@dataclass
class LocaleCacheModel(DataClassJsonMixin):
    emoji: str
    name: str
    code: str
