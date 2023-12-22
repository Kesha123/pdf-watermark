import os
import math
from jinja2 import Environment, FileSystemLoader

PDF_CONSTANT = 7.2

class File:

    def __init__(self, file_path: str = None):
        self.__file = file_path
        self.wm_command = f"gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -dAutoRotatePages=/None -sOutputFile=wm_{self.__file} wm.ps {self.__file}"

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
        return min( info[0]/text_length, info[1]/text_length )

    def __character_size(self, text_length, info):
        return math.sqrt(2 * math.pow( self.__min_dimension(info, text_length), 2 ))

    def __text_box_width(self, text_length, info, rotate):
        return self.__min_dimension(info, text_length) * (text_length * math.cos(rotate) + math.sin(rotate))

    def watermarking(self, transparency: float = 0.5, text: str = "TOP SECRET", font: str = 'Helvetica-Bold', output_file: str = '') -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(current_dir, 'templates')
        file_loader = FileSystemLoader(templates_dir)
        env = Environment(loader=file_loader)
        template = env.get_template("./watermark_template.ps")

        pages_info = self.__get_info()

        output_command = f"gs -q -dNOPAUSE -sDEVICE=pdfwrite -dAutoRotatePages=/None -sOUTPUTFILE={ output_file if self.__validate_output_file(output_file) else 'wm_' + self.__file} -dBATCH "

        for index,info in enumerate(pages_info):
            wm = f"gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -dAutoRotatePages=/None -dFirstPage={index+1} -dLastPage={index+1} -sOutputFile={index}_{self.__file} wm.ps {self.__file}"

            text_length = len(text)
            character_size = self.__character_size(text_length, info)

            rotate = math.atan(info[1]/info[0])

            starting_X = self.__min_dimension(info, text_length) * math.sin(rotate) + (info[0] - self.__text_box_width(text_length, info, rotate)) * 0.5
            starting_Y = (min(info) - character_size * math.sin(rotate)) / 2

            position = f"{starting_X} {starting_Y}"

            size = character_size
            rotate_degrees = math.degrees(rotate)

            print(info, size, rotate_degrees, position)

            watermark = template.render(transparency=transparency, text=text, rotate=rotate_degrees, size=size, font=font, position=position)

            output_command += f"{index}_{self.__file} "

            with open("wm.ps",'w') as file:
                file.write(watermark)
                file.close()

            os.system(wm)
            os.remove("wm.ps")

        os.system(output_command)

        for i in range(0,len(pages_info)):
            os.remove(f"{i}_{self.__file}")
