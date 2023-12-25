import os
import math
import pdf_watermark.scripts.scripts as scripts
from jinja2 import Template
from pdf_watermark.constants.page import PageInfo


class Page:

    def __init__(self, number: int, page_info: PageInfo, file_path: str) -> None:
        self.__number = number
        self.__page_info = page_info
        self.__file = file_path

    def get_page_number(self) -> int:
        return self.__number

    def __min_dimension(self, info: PageInfo, text_length: int) -> float:
        return min( info.XDimension/text_length, info.YDimension/text_length )

    def __character_size(self, text_length: int, info: PageInfo) -> float:
        return math.sqrt(2 * math.pow( self.__min_dimension(info, text_length), 2 ))

    def __text_box_width(self, text_length: int, info: PageInfo, rotate: float) -> float:
        return self.__min_dimension(info, text_length) * (text_length * math.cos(rotate) + math.sin(rotate))

    def __text_box_height(self, text_length: int, info: PageInfo, rotate: float) -> float:
        return self.__min_dimension(info, text_length) * (text_length * math.cos(rotate) + math.sin(rotate))

    async def apply_watermark_async(self, lock_dir: str, template: Template, transparency: float = 0.5, text: str = "TOP SECRET", font: str = 'Helvetica-Bold') -> None:
        gs_watermark_script = "wm.ps"

        wm = scripts.extract_page(
            first_page = self.__number,
            last_page = self.__number,
            output_file = f"{lock_dir}/{self.__number}.pdf",
            gs_script = gs_watermark_script,
            file_name = self.__file
        )

        text_length = len(text)
        size = self.__character_size(text_length, self.__page_info)
        rotate = math.atan( self.__page_info.YDimension / self.__page_info.XDimension )
        starting_X = self.__min_dimension(self.__page_info, text_length) * math.sin(rotate) + (self.__page_info.XDimension - self.__text_box_width(text_length, self.__page_info, rotate)) * 0.5
        starting_Y = (self.__page_info.YDimension - self.__text_box_height(text_length, self.__page_info, rotate) ) * 0.5
        position = f"{starting_X} {starting_Y}"

        rotate_degrees = math.degrees(rotate)
        watermark = template.render(transparency=transparency, text=text, rotate=rotate_degrees, size=size, font=font, position=position)

        with open(gs_watermark_script,'w') as file:
            file.write(watermark)
            file.close()

        os.system(wm)
        os.remove(gs_watermark_script)

    def apply_watermark(self, lock_dir: str, template: Template, transparency: float = 0.5, text: str = "TOP SECRET", font: str = 'Helvetica-Bold') -> None:
        gs_watermark_script = "wm.ps"

        wm = scripts.extract_page(
            first_page = self.__number,
            last_page = self.__number,
            output_file = f"{lock_dir}/{self.__number}.pdf",
            gs_script = gs_watermark_script,
            file_name = self.__file
        )

        text_length = len(text)
        size = self.__character_size(text_length, self.__page_info)
        rotate = math.atan( self.__page_info.YDimension / self.__page_info.XDimension )
        starting_X = self.__min_dimension(self.__page_info, text_length) * math.sin(rotate) + (self.__page_info.XDimension - self.__text_box_width(text_length, self.__page_info, rotate)) * 0.5
        starting_Y = (self.__page_info.YDimension - self.__text_box_height(text_length, self.__page_info, rotate) ) * 0.5
        position = f"{starting_X} {starting_Y}"

        rotate_degrees = math.degrees(rotate)
        watermark = template.render(transparency=transparency, text=text, rotate=rotate_degrees, size=size, font=font, position=position)

        with open(gs_watermark_script,'w') as file:
            file.write(watermark)
            file.close()

        os.system(wm)
        os.remove(gs_watermark_script)