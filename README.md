# PDF Watermark

**PDF Watermark** provides functionality for applying watermarks to PDF files. This library exclusively utilizes `Python` and `Ghostscript`.

## Install
```
pip install git+https://github.com/Kesha123/pdf-watermark.git@v<latest-release-tag-number>
```

## Classes and methods

### File
| Argument | Type | Default value | Description |
|---|---|---|---|
| **file_path** | str | None | Path to pdf file you want to apply watermark for |

`watermarking`
| Argument | Type | Default value | Description |
|---|---|---|---|
| **transparency** | float | 0.5 | Watermark transparency level |
| **text** | str | 'TOP SECRET' | Watermark text |
| **font** | str | Helvetica-Bold | Watermark font |
| **output_file** | str | None | Output file name |


## Use
```python
from pdf_watermark.watermark import File

pdf_file_path = "/path/to/file.pdf"

file = File(file_path=pdf_file_path)
file.watermarking()
```