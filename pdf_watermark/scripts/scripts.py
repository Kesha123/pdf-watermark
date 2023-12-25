from pdf_watermark.constants.page import *


def get_file_information(file_name: str) -> str:
    return f"gs -q -dNODISPLAY -dQUIET -dNOSAFER -sFileName={file_name} -c \"FileName (r) file runpdfbegin 1 1 pdfpagecount {{pdfgetpage /MediaBox get {{=print ( ) print}} forall (\\n) print}} for quit\""

def resize_file(file_name: str, page_size: PageSize) -> str:
    return f"gs -q -o r_{file_name} -sDEVICE=pdfwrite -sPAPERSIZE={page_size} -dPDFFitPage -dCompatibilityLevel=1.4 {file_name}"

def extract_page(first_page: str, last_page: str, output_file: str, gs_script: str, file_name: str) -> str:
    return f"gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -dAutoRotatePages=/None -dFirstPage={first_page} -dLastPage={last_page} -sOutputFile={output_file} {gs_script} {file_name} 2>/dev/null"

def concat_files(output_file: str) -> str:
    return f"gs -q -dNOPAUSE -sDEVICE=pdfwrite -dAutoRotatePages=/None -sOUTPUTFILE={output_file} -dBATCH 2>/dev/null"