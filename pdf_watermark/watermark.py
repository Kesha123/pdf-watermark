import os
import math
import uuid
import shutil
from pdf_watermark.scripts.scripts import *
from jinja2 import Environment, FileSystemLoader
from pdf_watermark.constants.page import PageSize, PageInfo


class File:

    def __init__(self, file_path: str = None) -> None:
        self.__file = file_path

    def __get_info(self) -> PageInfo:
        pages_info = get_file_information(self.__file)
        exec = os.popen(pages_info)
        out = exec.read()
        return [ PageInfo(XDimension=float(page.split(' ')[2]), YDimension=float(page.split(' ')[3])) for page in out.rstrip().split('\n') ]

    def __resize(self, file_name: str, page_size: PageSize) -> None:
        command = resize_file(file_name, page_size)
        os.system(command)

    def __validate_output_file(self, output_file: str) -> bool:
        return output_file.split('.')[-1] == "pdf"

    def __min_dimension(self, info: PageInfo, text_length: int) -> float:
        return min( info.XDimension/text_length, info.YDimension/text_length )

    def __character_size(self, text_length: int, info: PageInfo) -> float:
        return math.sqrt(2 * math.pow( self.__min_dimension(info, text_length), 2 ))

    def __text_box_width(self, text_length: int, info: PageInfo, rotate: float) -> float:
        return self.__min_dimension(info, text_length) * (text_length * math.cos(rotate) + math.sin(rotate))

    def __text_box_height(self, text_length: int, info: PageInfo, rotate: float) -> float:
        return self.__min_dimension(info, text_length) * (text_length * math.cos(rotate) + math.sin(rotate))

    def __get_template(self, template_name: str = "./watermark_template.ps"):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(current_dir, 'templates')
        file_loader = FileSystemLoader(templates_dir)
        env = Environment(loader=file_loader)
        return env.get_template(template_name)

    def watermarking(self, transparency: float = 0.5, text: str = "TOP SECRET", font: str = 'Helvetica-Bold', output_file: str = '') -> None:
        template = self.__get_template()
        pages_info = self.__get_info()
        lock_dir = f'.lock.{uuid.uuid4()}'

        os.mkdir(lock_dir)

        output_command = concat_files( output_file if self.__validate_output_file(output_file) else 'wm_' + self.__file )

        for index, info in enumerate(pages_info):
            gs_watermark_script = "wm.ps"

            wm = apply_waterwark(
                first_page = index+1,
                last_page = index+1,
                output_file = f"{lock_dir}/{index}_{self.__file}",
                gs_script = gs_watermark_script,
                file_name = self.__file
            )

            text_length = len(text)
            size = self.__character_size(text_length, info)
            rotate = math.atan( info.YDimension / info.XDimension )
            starting_X = self.__min_dimension(info, text_length) * math.sin(rotate) + (info.XDimension - self.__text_box_width(text_length, info, rotate)) * 0.5
            starting_Y = (info.YDimension - self.__text_box_height(text_length, info, rotate) ) * 0.5
            position = f"{starting_X} {starting_Y}"

            rotate_degrees = math.degrees(rotate)
            watermark = template.render(transparency=transparency, text=text, rotate=rotate_degrees, size=size, font=font, position=position)
            output_command += f"{lock_dir}/{index}_{self.__file} "

            with open(gs_watermark_script,'w') as file:
                file.write(watermark)
                file.close()

            os.system(wm)
            os.remove(gs_watermark_script)

        os.system(output_command)
        shutil.rmtree(lock_dir)
