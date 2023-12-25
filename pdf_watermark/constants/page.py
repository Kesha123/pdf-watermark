from enum import Enum
from dataclasses import dataclass, field


class PageOrientation(Enum):
    PORTRAIT = 'portrait'
    LANDSCAPE = 'landscape'


@dataclass
class PageInfo:
    XDimension: float
    YDimension: float
    Orientation: PageOrientation = field(default_factory = lambda: PageOrientation.PORTRAIT)