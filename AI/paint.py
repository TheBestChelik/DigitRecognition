import time
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageDraw
from AI import Recognizer
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from train import *

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.canvas_width = 560
        self.canvas_height = 560
        self.brush_size = self.canvas_width / 28
        self.brush_color = "black"

        self.recognizer = Recognizer()
        self.model_files = glob.glob(f"*.model")

        # Create the canvas on the left side
        self.canvas = Canvas(
            self.root,
            bg="white",
            width=self.canvas_width,
            height=self.canvas_height
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Create a container frame for the tab control on the right side
        tab_frame = Frame(self.root)
        tab_frame.grid(row=0, column=1, sticky="nsew")

        # Create the tab control
        self.tab_control = Notebook(tab_frame)
        self.tab_control.pack(fill=BOTH, expand=True)

        # Create the "Recognize" page
        recognize_page = Frame(self.tab_control)
        self.tab_control.add(recognize_page, text="Recognize")
        self.add_recognize_controls(recognize_page)

        # Create the "Train" page
        train_page = Frame(self.tab_control)
        self.tab_control.add(train_page, text="Train")
        self.add_train_controls(train_page)

        # Create the "Update Model" page
        update_model_page = Frame(self.tab_control)
        self.tab_control.add(update_model_page, text="Update Model")
        self.add_update_model_controls(update_model_page)

        # Set the grid weights to expand the canvas and tab control
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Bind events to the canvas
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.export)
        self.canvas.bind("<Button-3>", self.rightClick)
        self.canvas.bind("<Return>", self.enter_pressed)

        self.NumDigitsAdded = 0

    def enter_pressed(self, event):
        if(self.tab_control.index(self.tab_control.select())== 1 and self.model_textbox.get()!=""):
            self.ImageDrawn()

    def add_update_model_controls(self, parent):
        # Add controls for the "Update Model" page
        self.error_label_updator = Label(parent, text="", foreground="red")
        self.error_label_updator.pack(side=TOP, padx=10, pady=10)

        # Create a frame to hold the label and combobox
        label_frame = Frame(parent)
        label_frame.pack(side=TOP, padx=10, pady=10)

        # Add the label "Model" to the label frame
        model_label = Label(label_frame, text="Model:")
        model_label.pack(side=TOP)

        # Add the combobox to the label frame
        self.label_combobox_updator = Combobox(
            label_frame,
            values=self.model_files,
            state="readonly",
            width=15
        )
        self.label_combobox_updator.pack(side=TOP, anchor=NE)
        self.label_combobox_updator.bind("<<ComboboxSelected>>", lambda event, widget=self.label_combobox_updator: self.ChangeModel(event, widget))

        # Add a big textbox for update
        self.update_textbox = Text(parent, height=1, width=1, font=("Arial", 64))
        self.update_textbox.pack()

        self.update_textbox.bind("<Key>", self.validate_input)
        # Add a "Save" button
        self.save_button_update = Button(parent, text="Save", command=self.SaveUpdate)
        self.save_button_update.pack()
        # Add a "Retrain" button
        self.retrain_button = Button(parent, text="Retrain", command=self.train_button_pressed)
        self.retrain_button.pack()

        # Add a label for the number of digits added
        label = Label(parent, text="Digits added:")
        label.pack()
        self.NumDigitsAdded_label = Label(parent, text="0", font=("Arial", 24))
        self.NumDigitsAdded_label.pack()
        # Add a frame to hold the digit label and align it vertically
        label_frame = Frame(parent)
        label_frame.pack(side=TOP, pady=0, fill=BOTH, expand=True)

        # Add a frame to center the digit label vertically and horizontally
        center_frame = Frame(label_frame)
        center_frame.pack(expand=True)


    def SaveUpdate(self):
        print(self.update_textbox.get("1.0", "end"))
        filename = f"{self.update_textbox.get('1.0', 'end-1c')}_{int(time.time())}"
        self.SaveImage(self.canvas, dirname=self.label_combobox_updator.get()[:-6], filename=filename)
        self.clear_canvas()
        self.NumDigitsAdded+=1
        self.NumDigitsAdded_label.config(text=str(self.NumDigitsAdded))


    def validate_input(self, event):
        # Delete the existing text in the Text widget
        self.update_textbox.delete("1.0", "end")

        # Allow only digits (0-9), the Backspace key (ASCII code 8), and the Delete key (ASCII code 127)
        if event.char.isdigit() or event.keycode == 8 or event.keycode == 127:
            if event.keycode == 8 or event.keycode == 127:
                # Handle Backspace and Delete keys for removing characters
                # Check if there is any text selected
                if self.update_textbox.tag_ranges("sel"):
                    # Delete the selected text
                    self.update_textbox.delete("sel.first", "sel.last")
                elif event.keycode == 8:
                    # Handle Backspace key
                    # Delete the character to the left of the cursor
                    self.update_textbox.delete("insert-1c")
                elif event.keycode == 127:
                    # Handle Delete key
                    # Delete the character to the right of the cursor
                    self.update_textbox.delete("insert")

            # Append the new character to the Text widget
            self.update_textbox.insert("1.0", event.char)

        # Block the input
        return "break"

    def add_recognize_controls(self, parent):
        self.error_label_recognizer = Label(parent, text="", foreground="red")
        self.error_label_recognizer.pack(side=TOP, padx=10, pady=10)

        # Create a frame to hold the label and combobox
        label_frame = Frame(parent)
        label_frame.pack(side=TOP, padx=10, pady=10)

        # Add the label "Model" to the label frame
        model_label = Label(label_frame, text="Model:")
        model_label.pack(side=TOP)

        # Add the combobox to the label frame
        self.label_combobox = Combobox(
            label_frame,
            values=self.model_files,
            state="readonly",
            width=15
        )
        self.label_combobox.pack(side=TOP, anchor=NE)
        self.label_combobox.bind("<<ComboboxSelected>>", lambda event, widget=self.label_combobox: self.ChangeModel(event, widget))


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

    def ChangeModel(self, event, widget):
        self.NumDigitsAdded = 0
        self.recognizer.SetModel(widget.get())

    def add_train_controls(self, parent):
        # Add controls for the "Train" page     
        self.error_label = Label(parent, text="", foreground="red")
        self.error_label.pack()

        # Create a label and textbox for the model name
        self.model_label = Label(parent, text="Model name:")
        self.model_label.pack()
        self.model_textbox = Entry(parent)
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
        self.save_button = Button(parent, text="Save", command=self.ImageDrawn, state="disabled")
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
        self.train_button = Button(parent, text="Train", state="disabled", command=self.train_button_pressed)
        self.train_button.pack()
        self.model_textbox.bind("<KeyRelease>", self.CheckExistanceModel)


    def train_button_pressed(self):
        if self.tab_control.index(self.tab_control.select()) == 1:
            moduleName = self.model_textbox.get()
        else:
            moduleName = self.label_combobox_updator.get()[:-6]
        self.StartTrain(modelName=moduleName)
    

    def CheckExistanceModel(self, event):
        if(self.model_textbox.get() == ""):
            self.save_button.configure(state="disabled")
            self.digit_label.configure(text="")
            self.digit_progressbar_label.configure(text=f"Digit {0} of {10}")
            self.overall_progressbar_label.configure(text=f"Progress: 0 %")
            self.digit_progressbar.configure(value=0)
            self.overall_progressbar.configure(value=0)
        else:
            self.enable_controls()
            if os.path.exists(self.model_textbox.get()):
                self.error_label.configure(text="Model already exist!")
            else:
                self.error_label.configure(text="")
            
        
    def StartTrain(self, modelName):
        file_list = os.listdir(modelName)
        image_arrays = []
        y_train = []
        for file_name in file_list:
            image_arrays.append(np.invert(np.load(modelName+"/"+file_name)))
            #y_train = np.append(y_train, int(file_name[0]))
            y_train.append(int(file_name[0]))
        x_train = np.stack(image_arrays)
        y_train = np.stack(y_train)
        #print(type(y_train))
        #print(x_train.shape)
        self.train_button.configure(state="disabled")
        trainModel(x_train, y_train, modelName+".model")
        self.model_files.append(modelName+".model")
        self.train_button.configure(state="normal")


    def enable_controls(self):
        # Enable all the controls
        self.save_button.configure(state="normal")
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
        filename = f"{self.CurDigit}_{int(time.time())}"
        self.SaveImage(self.canvas,dirname=self.model_textbox.get(), filename=filename)
        self.clear_canvas()
        self.DigitNum+=1
        if(self.DigitNum==self.MaxCopiesOfDigit and self.CurDigit!=9):
            self.CurDigit += 1
            self.DigitNum = 0
        self.UpdateProgress()
        if(self.CurDigit == 9 and self.DigitNum == self.MaxCopiesOfDigit):
            self.save_button.configure(state="disabled")
            self.train_button.configure(state="normal")
    
    def SaveImage(self, canvas, dirname, filename):
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
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        np.save(f"{dirname}/{filename}", image_array)
        print(f"{dirname}/{filename} -saved")

    
    def draw(self, event):
        self.canvas.focus_set()
        if(self.canvas['state']!="normal"):
            return
        x1, y1 = (event.x - self.brush_size), (event.y - self.brush_size)
        x2, y2 = (event.x + self.brush_size), (event.y + self.brush_size)
        self.canvas.create_oval(x1, y1, x2, y2, fill=self.brush_color, width=self.brush_size)

    
    def export(self, event):
        if self.tab_control.index(self.tab_control.select()) == 1:
            return
        if self.tab_control.index(self.tab_control.select()) == 0:
            if(self.label_combobox.get() == ""):
                self.error_label_recognizer.configure(text="Select the model!")
                return
            else:
                self.error_label_recognizer.configure(text="")
            
        elif self.tab_control.index(self.tab_control.select())== 2:
            if(self.label_combobox_updator.get() == ""):
                self.error_label_updator.configure(text="Select the model!")
                return
            else:
                self.error_label_updator.configure(text="")
        
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
        if(self.tab_control.index(self.tab_control.select())== 0):
            self.recognize_digit_label.config(text=str(digit))
        elif self.tab_control.index(self.tab_control.select())== 2:
            self.update_textbox.delete("1.0", "end")
            self.update_textbox.insert("1.0", str(digit))

    def rightClick(self, event):
        self.clear_canvas()

    def clear_canvas(self):
        self.canvas.delete("all")
    
if __name__ == "__main__":
    root = Tk()
    paint_app = PaintApp(root)
    root.mainloop()