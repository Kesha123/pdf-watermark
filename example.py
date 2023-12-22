from pdf_watermark.watermark import File

file1 = File(file_path="test.pdf")
file1.watermarking()

file2 = File(file_path="test-2.pdf")
file2.watermarking()