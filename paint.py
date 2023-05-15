from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageDraw
from digitRecogniser import Recognizer
import numpy as np

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.canvas_width = 560
        self.canvas_height = 560
        self.brush_size = self.canvas_width/28
        self.brush_color = "black"
        
        self.recognizer = Recognizer()

        # Create the tab control and add the pages
        self.tab_control = Notebook(self.root)
        self.tab_control.pack(side=TOP, fill=BOTH, expand=True)
        
        # Create the "Recognize" page
        recognize_page = Frame(self.tab_control)
        self.tab_control.add(recognize_page, text="Recognize")
        self.add_recognize_controls(recognize_page)
        
        # Create the "Train" page
        train_page = Frame(self.tab_control)
        self.tab_control.add(train_page, text="Train")
        self.add_train_controls(train_page)

        
    def add_recognize_controls(self, parent):
        # Add the canvas to the "Recognize" page
        self.recognize_canvas = Canvas(
            parent,
            bg="white",
            width=self.canvas_width,
            height=self.canvas_height
        )
        self.recognize_canvas.pack(side=LEFT)

        # Add the dropdown list to the top right corner
        options = ["Option 1", "Option 2", "Option 3"]
        
        # Create a frame to hold the label and combobox
        label_frame = Frame(parent)
        label_frame.pack(side=TOP, padx=10, pady=10)
        
        # Add the label "Model" to the label frame
        model_label = Label(label_frame, text="Model:")
        model_label.pack(side=TOP)
        
        # Add the combobox to the label frame
        self.label_combobox = Combobox(
            label_frame,
            values=options,
            state="readonly",
            width=15
        )
        self.label_combobox.pack(side=TOP, anchor=NE)
        
        # Add a frame to hold the digit label and align it vertically
        label_frame = Frame(parent)
        label_frame.pack(side=TOP, pady=0, fill=BOTH, expand=True)
        
        # Add a frame to center the digit label vertically and horizontally
        center_frame = Frame(label_frame)
        center_frame.pack(expand=True)
        
        # Add the digit label to the "Recognize" page
        self.recognize_digit_label = Label(
            center_frame,
            text="",
            font=("Arial", 64)  # Increase the font size
        )
        self.recognize_digit_label.pack()
        
        # Bind events to the canvas
        self.recognize_canvas.bind("<B1-Motion>", lambda event, widget=self.recognize_canvas: self.draw(widget, event))
        self.recognize_canvas.bind("<ButtonRelease-1>", lambda event, widget=self.recognize_canvas: self.export(widget, event))
        self.recognize_canvas.bind("<Button-3>", lambda event, widget=self.recognize_canvas: self.rightClick(widget, event))
        
    def add_train_controls(self, parent):
        # Add the canvas to the "Train" page with the same size as in the "Recognize" page
        self.train_canvas = Canvas(
            parent,
            bg="white",
            width=self.canvas_width,
            height=self.canvas_height
        )
        self.train_canvas.pack(side=LEFT)
        
        # Create a label and textbox for the model name
        model_label = Label(parent, text="Model name:")
        model_label.pack()
        model_textbox = Entry(parent)
        model_textbox.pack()
        
        # Add some space between the textbox and the "Write digit:" label
        space_label = Label(parent, text="")
        space_label.pack()
        
        # Create a label for the "Write digit:" text
        write_digit_label = Label(parent, text="Write digit:")
        write_digit_label.pack()
        
        # Create a label to display the digit being written (with big font size)
        self.digit_label = Label(parent, text="7", font=("Helvetica", 36))
        self.digit_label.pack()
        
        # Create a "Save" button
        save_button = Button(parent, text="Save")
        save_button.pack()
        
        # Add some space between the "Save" button and the progress bars
        space_label2 = Label(parent, text="")
        space_label2.pack()
        
        # Create a progressbar for digit count
        digit_progressbar_label = Label(parent, text="Digit 7 of 10")
        digit_progressbar_label.pack()
        digit_progressbar = Progressbar(parent, orient="horizontal", length=100, mode="determinate")
       
        digit_progressbar.pack()
        digit_progressbar.configure(value=30)

        # Create a progressbar for overall progress
        overall_progressbar_label = Label(parent, text="Progress: 77 of 100")
        overall_progressbar_label.pack()
        overall_progressbar = Progressbar(parent, orient="horizontal", length=100, mode="determinate")
        overall_progressbar.pack()
        overall_progressbar.configure(value = 77)
        
        # Create a "Train" button
        train_button = Button(parent, text="Train")
        train_button.pack()
        
        self.train_canvas.bind("<B1-Motion>", lambda event, widget=self.train_canvas: self.draw(widget, event))
        #self.train_canvas.bind("<ButtonRelease-1>", self.export)
        self.train_canvas.bind("<Button-3>", lambda event, widget=self.train_canvas: self.rightClick(widget, event))




    def draw(self, widget, event):
        x1, y1 = (event.x - self.brush_size), (event.y - self.brush_size)
        x2, y2 = (event.x + self.brush_size), (event.y + self.brush_size)
        widget.create_oval(x1, y1, x2, y2, fill=self.brush_color, width=self.brush_size)

    
    def export(self, widget, event):
         # Create a blank image of size 28x28
        image = Image.new('L', (560, 560), color=255)
        
        # Create a drawing object
        draw = ImageDraw.Draw(image)
        
        # Iterate over all items on the canvas
        items = widget.find_all()
        for item in items:
            # Get the coordinates of the item
            x1, y1, x2, y2 = widget.coords(item)
            
            # Draw a rectangle on the image using the coordinates
            draw.rectangle([x1, y1, x2, y2], fill=0)
        
        # Resize the image to 28x28 pixels
        image = image.resize((28, 28), Image.LANCZOS)
        
        # Convert the image to a NumPy array
        image_array = np.array(image)
        
        # Perform digit recognition using the Recognizer object
        digit = self.recognizer.Recognize(image_array)
    
        # Update the DigitLabel text
        self.recognize_digit_label.config(text=str(digit))

    def rightClick(self, widget, event):
        self.clear_canvas(widget)

    def clear_canvas(self, widget):
        widget.delete("all")
    
if __name__ == "__main__":
    root = Tk()
    paint_app = PaintApp(root)
    root.mainloop()
