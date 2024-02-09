import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pdf_watermark',
    version='0.0.1',
    author='Innokentii Kozlov',
    author_email='innokentiikozlov@gmail.com',
    description='PDF watermarking tool',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Kesha123/pdf-watermark',
    license='MIT',
    packages=['pdf_watermark', 'pdf_watermark.constants', 'pdf_watermark.templates', 'pdf_watermark.scripts', 'pdf_watermark.utils'],
    install_requires=[
        "Jinja2==3.1.2",
        "numpy==1.26.2",
        "opencv-python==4.8.1.78"
    ]
)