import cv2
import numpy as np
from pdf_watermark.constants.ascii import CHARS_BY_DENSITY

COLS = 240
SCALE = 0.4

def alpha_channle_image(image_path: str, output_image_path: str, transparency_factor: float) -> None:
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image.shape[2] == 3:
        alpha_channel = np.ones((image.shape[0], image.shape[1]), dtype=np.uint8) * 255
        image = np.dstack((image, alpha_channel))
    image[:, :, 3] = (image[:, :, 3] * transparency_factor).astype(np.uint8)
    cv2.imwrite(output_image_path, image)


def getAverageL(image):
    im = np.array(image)
    w,h = im.shape
    return np.average(im.reshape(w*h))


def image_to_ascii(image_path: str) -> list[str]:
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    W, H = image.shape[1], image.shape[0]
    width = W/COLS
    height = width/SCALE
    rows = int(H/height)

    ascii_image = []
    for j in range(rows):
        y1 = int(j*height)
        y2 = int((j+1)*height)
        if j == rows - 1:
            y2 = H
        ascii_image.append("")
        for i in range(COLS):
            x1 = int(i*width)
            x2 = int((i+1) * width)
            if i == COLS - 1:
                x2 = W

            img = image[y1:y2+1, x1:x2+1]
            avg = int(getAverageL(img))
            gsval = CHARS_BY_DENSITY[int((avg*69)/255)]
            ascii_image[j] += gsval

        ascii_image[j] = ascii_image[j].replace("Q", " ")

    return ascii_image


def image_to_ascii_color(image_path: str) -> None:
    raise NotImplementedError