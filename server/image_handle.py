import io
from tkinter import *
from PIL import Image, ImageDraw


IMAGE_FILE_NAME = 'image.jpeg'


class ImageHandle:
    # Used to draw on a virtual image which will be displayed in the client
    def __init__(self, w: int, h: int, bgcolor=(255, 255, 255)):
        self.w = w
        self.h = h
        self.bgcolor = bgcolor
        self.image = Image.new("RGB", (w, h), bgcolor)
        self.draw = ImageDraw.Draw(self.image)
        self.brush_size = 3
        self.last_x = 0
        self.last_y = 0
        self.max_distance2 = 100**2  # max distance between two consecutive points (squared)

    def paint(self, x, y):
        # prevent lines that are too quick
        if self.dist2(x, y) < self.max_distance2:
            self.draw.line([(self.last_x, self.last_y), (x, y)], fill="black", width=self.brush_size)
        self.last_x = x
        self.last_y = y

    def clear(self):
        self.image = Image.new("RGB", (self.w, self.h), self.bgcolor)
        self.draw = ImageDraw.Draw(self.image)

    @property
    def image_bytes(self) -> bytes:
        img_byte_arr = io.BytesIO()
        self.image.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()

    def dist2(self, x, y) -> float:
        return abs((self.last_x - x) ** 2 + (self.last_y - y) ** 2)

    def save(self):
        self.image.save(IMAGE_FILE_NAME)
