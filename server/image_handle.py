import io
from tkinter import *
from PIL import Image, ImageDraw


class ImageHandle:
    # Used to draw on a virtual image which will be displayed in the client
    def __init__(self, w: int, h: int, bgcolor=(255, 255, 255)):
        self.image = Image.new("RGB", (w, h), bgcolor)
        self.draw = ImageDraw.Draw(self.image)
        self.brush_size = 3

    def paint(self, x, y):
        x1, y1 = (x - self.brush_size), (y - self.brush_size)
        x2, y2 = (x + self.brush_size), (y + self.brush_size)
        self.draw.ellipse([x1, y1, x2, y2], (0, 0, 0))

    @property
    def image_bytes(self) -> bytes:
        img_byte_arr = io.BytesIO()
        self.image.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()
