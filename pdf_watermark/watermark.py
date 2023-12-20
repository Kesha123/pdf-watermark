import os
import math
from jinja2 import Environment, FileSystemLoader

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

    def watermarking(self, transparency: float = 0.5, text: str = "TOP SECRET", font: str = 'Helvetica-Bold') -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(current_dir, 'templates')
        file_loader = FileSystemLoader(templates_dir)
        env = Environment(loader=file_loader)
        template = env.get_template("./watermark_template.ps")

        pages_info = self.__get_info()

        output_command = f"gs -q -dNOPAUSE -sDEVICE=pdfwrite -dAutoRotatePages=/None -sOUTPUTFILE=wm_{self.__file} -dBATCH "

        for index,info in enumerate(pages_info):
            wm = f"gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -dAutoRotatePages=/None -dFirstPage={index+1} -dLastPage={index+1} -sOutputFile={index}_{self.__file} wm.ps {self.__file}"

            position = f"{info[0]//7.2} {info[1]//7.2}"
            rotate = math.degrees(math.atan(info[1]/info[0]))
            size = math.sqrt(info[0]**2 + info[1]**2)//7.2

            print(info, size, rotate, position)

            watermark = template.render(transparency=transparency, text=text, rotate=rotate, size=size, font=font, position=position)

            output_command += f"{index}_{self.__file} "

            with open("wm.ps",'w') as file:
                file.write(watermark)
                file.close()

            os.system(wm)
            os.remove("wm.ps")

        os.system(output_command)

        for i in range(0,len(pages_info)):
            os.remove(f"{i}_{self.__file}")
