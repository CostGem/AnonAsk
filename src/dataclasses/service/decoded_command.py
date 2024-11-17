from dataclasses import dataclass
from typing import Optional


@dataclass
class DecodedCommand:
    command: str
    args: Optional[str] = None
