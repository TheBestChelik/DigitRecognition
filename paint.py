from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageDraw
from digitRecogniser import Recognizer
import numpy as np
import matplotlib.pyplot as plt
import os
from train import *

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.canvas_width = 560
        self.canvas_height = 560
        self.brush_size = self.canvas_width/28
        self.brush_color = "black"
        
        self.recognizer = Recognizer("Hyi.model")

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
            height=self.canvas_height,
            state="disabled"
        )
        self.train_canvas.pack(side=LEFT)
        
        # Create a "Create new model" button
        create_model_button = Button(parent, text="Create new model", command=self.enable_controls)
        create_model_button.pack()
        
        # Create a label and textbox for the model name
        self.model_label = Label(parent, text="Model name:")
        self.model_label.pack()
        self.model_textbox = Entry(parent, state="disabled")
        self.model_textbox.pack()
        
        # Add some space between the textbox and the "Write digit:" label
        space_label = Label(parent, text="")
        space_label.pack()
        
        # Create a label for the "Write digit:" text
        write_digit_label = Label(parent, text="Write digit:")
        write_digit_label.pack()
        
        # Create a label to display the digit being written (with big font size)
        self.digit_label = Label(parent, text="", font=("Helvetica", 36))
        self.digit_label.pack()
        
        # Create a "Save" button
        self.save_button = Button(parent, text="Save", state="disabled", command=self.ImageDrawn)
        self.save_button.pack()
        
        # Add some space between the "Save" button and the progress bars
        space_label2 = Label(parent, text="")
        space_label2.pack()
        
        # Create a progressbar for digit count
        self.digit_progressbar_label = Label(parent, text="Digit 0 of 10")
        self.digit_progressbar_label.pack()
        self.digit_progressbar = Progressbar(parent, orient="horizontal", length=100, mode="determinate")
        self.digit_progressbar.pack()
        
        # Create a progressbar for overall progress
        self.overall_progressbar_label = Label(parent, text="Progress: 0%")
        self.overall_progressbar_label.pack()
        self.overall_progressbar = Progressbar(parent, orient="horizontal", length=100, mode="determinate")
        self.overall_progressbar.pack()
        
        # Create a "Train" button
        self.train_button = Button(parent, text="Train", command=self.StartTrain)
        self.train_button.pack()

        training_progressbar = Progressbar(parent, orient="horizontal", length=100, mode="determinate")
        training_progressbar.pack()
        
        self.train_canvas.bind("<B1-Motion>", lambda event, widget=self.train_canvas: self.draw(widget, event))
        #self.train_canvas.bind("<ButtonRelease-1>", self.export)
        self.train_canvas.bind("<Button-3>", lambda event, widget=self.train_canvas: self.rightClick(widget, event))

    def StartTrain(self):
        file_list = os.listdir(self.model_textbox.get())
        image_arrays = []
        y_train = []
        for file_name in file_list:
            image_arrays.append(np.invert(np.load(self.model_textbox.get()+"/"+file_name)))
            #y_train = np.append(y_train, int(file_name[0]))
            y_train.append(int(file_name[0]))
        x_train = np.stack(image_arrays)
        y_train = np.stack(y_train)
        print(type(y_train))
        print(x_train.shape)
        trainModel(x_train, y_train, self.model_textbox.get()+".model")


    def enable_controls(self):
        # Enable all the controls
        self.model_textbox.configure(state="normal")
        self.save_button.configure(state="normal")
        self.train_canvas.configure(state="normal")
        self.CurDigit = 0
        self.DigitNum = 0
        self.MaxCopiesOfDigit = 10
        self.UpdateProgress()

        
    def UpdateProgress(self):
        self.digit_label.configure(text=str(self.CurDigit))
        digit_progress = round(self.DigitNum/self.MaxCopiesOfDigit * 100)
        overall_progress = round((self.CurDigit*self.MaxCopiesOfDigit+self.DigitNum)/(10*self.MaxCopiesOfDigit)*100)
        self.digit_progressbar_label.configure(text=f"Digit {self.DigitNum} of {self.MaxCopiesOfDigit}")
        self.overall_progressbar_label.configure(text=f"Progress: {overall_progress} %")
        self.digit_progressbar.configure(value=digit_progress)
        self.overall_progressbar.configure(value=overall_progress)
    
    def ImageDrawn(self):
        self.SaveImage(self.train_canvas)
        self.DigitNum+=1
        if(self.DigitNum==self.MaxCopiesOfDigit and self.CurDigit!=9):
            self.CurDigit += 1
            self.DigitNum = 0
        self.UpdateProgress()
        if(self.CurDigit == 9 and self.DigitNum == self.MaxCopiesOfDigit):
            self.save_button.configure(state="disabled")
            self.train_button.configure(state="normal")
    
    def SaveImage(self, canvas):
        image = Image.new('L', (560, 560), color=255)
        
        # Create a drawing object
        draw = ImageDraw.Draw(image)
        
        # Iterate over all items on the canvas
        items = canvas.find_all()
        for item in items:
            # Get the coordinates of the item
            x1, y1, x2, y2 = canvas.coords(item)
            
            # Draw a rectangle on the image using the coordinates
            draw.rectangle([x1, y1, x2, y2], fill=0)
        
        # Resize the image to 28x28 pixels
        image = image.resize((28, 28), Image.LANCZOS)
        
        # Convert the image to a NumPy array
        image_array = np.array(image)
        if not os.path.exists(f"{self.model_textbox.get()}"):
            os.mkdir(self.model_textbox.get())
        np.save(f"{self.model_textbox.get()}/{self.CurDigit}_{self.DigitNum}", image_array)

    
    def draw(self, widget, event):
        if(widget['state']!="normal"):
            return
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
