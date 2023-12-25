# PDF Watermark

**PDF Watermark** provides functionality for applying watermarks to PDF files. This library exclusively utilizes `Python` and `Ghostscript`.

## Requirements

### Linux

#### Debian

```
sudo apt-get update
sudo apt-get install ghostscript
```
```
gs --version
```

#### RedHat

```
sudo yum install ghostscript
```
```
gs --version
```

### Windows
 - [ ] Install GhostScript https://www.ghostscript.com/download/gsdnld.html
 - [ ] After installation, you need to set up the `PATH` environment variable to include the directory where Ghostscript is installed.

### MacOS
```
brew install ghostscript
```
```
gs --version
```

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

#### Ouput
```bash
.
├── test.pdf
└── wm_test.pdf
```

## Calculations

### X Axis Positioning
 ![Main1](/images/x-axis-calcs.jpg)