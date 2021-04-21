from tkinter import *

from PIL import Image, ImageDraw


class ImageDrawer:
    # start a tkinter paint window to draw live images in the browser
    # for testing only
    def __init__(self, w: int, h: int):
        self.root = Tk()
        self.root.title("Paint Application")
        self.root.geometry(f"{w}x{h}")

        # create canvas
        self.wn = Canvas(self.root, width=w, height=h, bg='white')

        # PIL create an empty image and draw object to draw on
        # memory only, not visible
        self.image = Image.new("RGB", (w, h), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)

        # bind mouse event with canvas(wn)
        self.wn.bind('<B1-Motion>', self.paint)
        self.wn.pack()
        self.is_running = False

    def run(self):
        self.is_running = True
        self.root.mainloop()
        self.is_running = False

    def paint(self, event):
        # get x1, y1, x2, y2 co-ordinates
        x1, y1 = (event.x - 3), (event.y - 3)
        x2, y2 = (event.x + 3), (event.y + 3)
        color = "black"
        # display the mouse movement inside canvas
        self.wn.create_oval(x1, y1, x2, y2, fill=color, outline=color)
        self.draw.ellipse([x1, y1, x2, y2], (0, 0, 0))


if __name__ == "__main__":
    ImageDrawer(500, 500).run()
