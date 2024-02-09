from enum import Enum
from dataclasses import dataclass, field


@dataclass
class WaterMark:
    x: float
    y: float
    text: str
    font: str
    text_size: float
    transparency: float
