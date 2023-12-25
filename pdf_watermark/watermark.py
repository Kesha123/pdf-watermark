import os
import math
import uuid
import shutil
from jinja2 import Environment, FileSystemLoader

PDF_CONSTANT = 7.2

class File:

    def __init__(self, file_path: str = None):
        self.__file = file_path

    def __get_info(self):
        pages_info = f"gs -q -dNODISPLAY -dQUIET -dNOSAFER -sFileName={self.__file} -c \"FileName (r) file runpdfbegin 1 1 pdfpagecount {{pdfgetpage /MediaBox get {{=print ( ) print}} forall (\\n) print}} for quit\""
        exec = os.popen(pages_info)
        out = exec.read()
        return [(float(page.split(' ')[2]), float(page.split(' ')[3])) for page in out.rstrip().split('\n')]

    def __resize(self):
        resize_command = f"gs -q -o r_{self.__file}  -sDEVICE=pdfwrite  -sPAPERSIZE=a4  -dPDFFitPage  -dCompatibilityLevel=1.4  {self.__file}"
        os.system(resize_command)

    def __validate_output_file(self, output_file: str):
        return output_file.split('.')[-1] == "pdf"

    def __min_dimension(self, info, text_length):
        '''
        On image: m
        '''
        return min( info[0]/text_length, info[1]/text_length )

    def __character_size(self, text_length, info):
        return math.sqrt(2 * math.pow( self.__min_dimension(info, text_length), 2 ))

    def __text_box_width(self, text_length, info, rotate):
        '''
        On image: b = k + c
        '''
        return self.__min_dimension(info, text_length) * (text_length * math.cos(rotate) + math.sin(rotate))

    def __text_box_height(self, text_length, info, rotate):
        '''
        Same as __text_box_width (assuming character box is a square, which almost true)
        '''
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

        output_command = f"gs -q -dNOPAUSE -sDEVICE=pdfwrite -dAutoRotatePages=/None -sOUTPUTFILE={ output_file if self.__validate_output_file(output_file) else 'wm_' + self.__file} -dBATCH "

        for index,info in enumerate(pages_info):
            '''
            On image:
                rotate = alpha;
                starting_X = k + c;
            '''
            wm = f"gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -dAutoRotatePages=/None -dFirstPage={index+1} -dLastPage={index+1} -sOutputFile={lock_dir}/{index}_{self.__file} wm.ps {self.__file}"

            text_length = len(text)
            size = self.__character_size(text_length, info)

            rotate = math.atan(info[1]/info[0])

            starting_X = self.__min_dimension(info, text_length) * math.sin(rotate) + (info[0] - self.__text_box_width(text_length, info, rotate)) * 0.5
            starting_Y = (info[1] - self.__text_box_height(text_length, info, rotate) ) * 0.5

            position = f"{starting_X} {starting_Y}"

            rotate_degrees = math.degrees(rotate)

            watermark = template.render(transparency=transparency, text=text, rotate=rotate_degrees, size=size, font=font, position=position)

            output_command += f"{lock_dir}/{index}_{self.__file} "

            with open("wm.ps",'w') as file:
                file.write(watermark)
                file.close()

            os.system(wm)
            os.remove("wm.ps")

        os.system(output_command)

        shutil.rmtree(lock_dir)
