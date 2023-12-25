from pdf_watermark.watermark import File

file1 = File(file_path="test.pdf")
file1.watermarking(transparency=0.8, text="TOP SECRET")
