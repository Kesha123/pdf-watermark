from enum import Enum
from dataclasses import dataclass, field


class PageSize(Enum):
    A4 = 'a4'
    A5 = 'a5'


class PageOrientation(Enum):
    PORTRAIT = 'portrait'
    LANDSCAPE = 'landscape'


@dataclass
class PageInfo:
    XDimension: float
    YDimension: float
    Orientation: PageOrientation = field(default_factory = lambda: PageOrientation.PORTRAIT)

    def __post_init__(self):
        self.Orientation = PageOrientation.PORTRAIT if self.XDimension <= self.YDimension else PageOrientation.LANDSCAPE