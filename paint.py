from tkinter import *
from PIL import Image, ImageDraw
from digitRecogniser import Recognizer
import numpy as np

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digit Recognizer")

        self.canvas_width = 560
        self.canvas_height = 560

        self.brush_size = 20
        self.brush_color = "black"

        self.recognizer = Recognizer()

        self.create_widgets()

    def create_widgets(self):
        # Create a frame to hold the buttons
        buttons_frame = Frame(self.root)
        buttons_frame.pack(side=TOP)

        # Create the clear button and pack it to the left side of the buttons frame
        self.clear_button = Button(
            buttons_frame,
            text="Clear",
            command=self.clear_canvas
        )
        self.clear_button.pack(side=LEFT)

        # Create a frame to hold the label
        label_frame = Frame(self.root)
        label_frame.pack(side=TOP)

        # Create the digit label with a larger font size and pack it to the label frame
        self.DigitLabel = Label(
            label_frame,
            text="",
            font=("Arial", 24)
        )
        self.DigitLabel.pack()
        
        # Create the canvas and pack it to the left side of the root window
        self.canvas = Canvas(
            self.root,
            bg="white",
            width=self.canvas_width,
            height=self.canvas_height,
        )
        self.canvas.pack(side=LEFT)

        # Bind the B1-Motion event to the draw method
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.export)
        self.canvas.bind("<Button-3>", self.rightClick)



    def draw(self, event):
        x1, y1 = (event.x - self.brush_size), (event.y - self.brush_size)
        x2, y2 = (event.x + self.brush_size), (event.y + self.brush_size)
        self.canvas.create_oval(x1, y1, x2, y2, fill=self.brush_color, width=self.brush_size)

    
    def export(self, event):
         # Create a blank image of size 28x28
        image = Image.new('L', (560, 560), color=255)
        
        # Create a drawing object
        draw = ImageDraw.Draw(image)
        
        # Iterate over all items on the canvas
        items = self.canvas.find_all()
        for item in items:
            # Get the coordinates of the item
            x1, y1, x2, y2 = self.canvas.coords(item)
            
            # Draw a rectangle on the image using the coordinates
            draw.rectangle([x1, y1, x2, y2], fill=0)
        
        # Resize the image to 28x28 pixels
        image = image.resize((28, 28), Image.LANCZOS)
        
        # Convert the image to a NumPy array
        image_array = np.array(image)
        
        # Perform digit recognition using the Recognizer object
        digit = self.recognizer.Recognize(image_array)
    
        # Update the DigitLabel text
        self.DigitLabel.config(text=str(digit))

    def rightClick(self, event):
        self.clear_canvas()

    def clear_canvas(self):
        self.canvas.delete("all")
        self.DigitLabel.config(text="")

if __name__ == "__main__":
    root = Tk()
    paint_app = PaintApp(root)
    root.mainloop()
