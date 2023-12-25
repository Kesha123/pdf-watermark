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
 - [ ] [Install GhostScript](https://www.ghostscript.com/download/gsdnld.html)
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

#### Sync
```python
from pdf_watermark.watermark import File

pdf_file_path = "/path/to/file.pdf"

file = File(file_path=pdf_file_path)
file.watermarking()
```

#### Async
```python
import asyncio
from pdf_watermark.watermark import File

pdf_file_path = "/path/to/file.pdf"

file = File(file_path=pdf_file_path)
asyncio.run(file.watermarking_async())

#### Or ####

async def test_async() -> None:
    file = File(file_path=pdf_file_path)
    await file.watermarking_async()

def main() -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(
        test_async()
    ))
    loop.close()

if __name__ == '__main__':
    main()

```

### File
| Argument | Type | Default value | Description |
|---|---|---|---|
| **file_path** | str | None | Path to pdf file you want to apply watermark for |


### File.watermarking() & File.watermarking_async()
| Argument | Type | Default value | Description |
|---|---|---|---|
| **transparency** | float | 0.5 | Watermark transparency level |
| **text** | str | 'TOP SECRET' | Watermark text |
| **font** | str | Helvetica-Bold | Watermark font |
| **output_file** | str | None | Output file name |

#### Ouput
```bash
.
├── test.pdf
└── wm_test.pdf
```

## Calculations

### X Axis Positioning
 ![Main1](/images/x-axis-calcs.jpg)