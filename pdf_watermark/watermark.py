import os
import math
import uuid
import shutil
import asyncio
from pdf_watermark.page import Page
import pdf_watermark.scripts.scripts as scripts
from jinja2 import Environment, FileSystemLoader, Template
from pdf_watermark.pdf_watermark_types.page import PageSize, PageInfo

import cv2
import numpy as np

from ascii_magic import AsciiArt

from pdf_watermark.utils.image import *


class File:

    def __init__(self, file_path: str = None) -> None:
        self.__file = file_path

    def __get_info(self) -> PageInfo:
        pages_info = scripts.get_file_information(self.__file)
        exec = os.popen(pages_info)
        out = exec.read()
        return [ PageInfo(XDimension=float(page.split(' ')[2]), YDimension=float(page.split(' ')[3])) for page in out.rstrip().split('\n') ]

    def __resize(self, file_name: str, page_size: PageSize) -> None:
        command = scripts.resize_file(file_name, page_size)
        os.system(command)

    def __validate_output_file(self, output_file: str) -> bool:
        return output_file.split('.')[-1] == "pdf"

    def __get_template(self, template_name: str = "./text_watermark_template.ps") -> Template:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(current_dir, 'templates')
        file_loader = FileSystemLoader(templates_dir)
        env = Environment(loader=file_loader)
        return env.get_template(template_name)

    def watermarking(self, transparency: float = 0.5, text: str = "TOP SECRET", font: str = 'Helvetica-Bold', output_file: str = '') -> None:
        pages = [ Page(number=i+1, page_info=info, file_path=self.__file) for i, info in enumerate(self.__get_info()) ]
        lock_dir = f'.lock.{uuid.uuid4()}'
        os.mkdir(lock_dir)
        command = f"{scripts.concat_files( output_file if self.__validate_output_file(output_file) else 'wm_' + self.__file )} {' '.join([ f'{lock_dir}/{page.get_page_number()}.pdf' for page in pages ])} "
        for p in pages:
            p.apply_watermark(lock_dir, self.__get_template(), transparency, text, font)
        os.system(command)
        shutil.rmtree(lock_dir)

    async def watermarking_async(self, transparency: float = 0.5, text: str = "TOP SECRET", font: str = 'Helvetica-Bold', output_file: str = '') -> None:
        pages = [ Page(number=i+1, page_info=info, file_path=self.__file) for i, info in enumerate(self.__get_info()) ]
        lock_dir = f'.lock.{uuid.uuid4()}'
        os.mkdir(lock_dir)
        command = f"{scripts.concat_files( output_file if self.__validate_output_file(output_file) else 'wm_' + self.__file )} {' '.join([ f'{lock_dir}/{page.get_page_number()}.pdf' for page in pages ])} "

        watermarking_tasks = [page.apply_watermark_async(lock_dir, self.__get_template(), transparency, text, font) for page in pages]
        await asyncio.gather(*watermarking_tasks)

        os.system(command)
        shutil.rmtree(lock_dir)

    def image_watermark(output_file: str, image_stamp_path: str, transparency: float = 0.5):
        raise NotImplementedError()

    def image_ascii_watermark(output_file: str, image_stamp_path: str, transparency: float = 0.5, monochrome: bool = True):
        ascii_art = image_to_ascii(image_stamp_path)
        for l in ascii_art:
            print(l)

    def image(self, output_file: str, stamp_path: str, transparency: float = 0.5):
        my_art = AsciiArt.from_image(stamp_path)
        ascii: str = my_art.to_terminal()

        ascii = ascii.replace('(', '[')
        ascii = ascii.replace(')', ']')

        pages = [ Page(number=i+1, page_info=info, file_path=self.__file) for i, info in enumerate(self.__get_info()) ]

        lock_dir = f'.lock.{uuid.uuid4()}'

        os.mkdir(lock_dir)

        command = f"{scripts.concat_files( output_file if self.__validate_output_file(output_file) else 'wm_' + self.__file )} {' '.join([ f'{lock_dir}/{page.get_page_number()}.pdf' for page in pages ])} "

        for p in pages:
            p.apply_watermark(lock_dir, self.__get_template(template_name="./image_watermark_template.ps"), transparency, ascii, '')

        os.system(command)
        shutil.rmtree(lock_dir)
