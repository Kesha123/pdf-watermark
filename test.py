from pdf_watermark.watermark import File


pdf_file_path = "practical-work-1.pdf"

file = File(file_path=pdf_file_path)
# file.watermarking(output_file="output-text.pdf", transparency=0.5, text="TOP SECRET")
# file.image(output_file="output-image.pdf", stamp_path="images/logo-transparent.png")

file.image_ascii_watermark(image_stamp_path="images/logo.png")
