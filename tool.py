import tkinter as tk
from subprocess import Popen
from tkinter import StringVar
import sys
from PIL import Image, ImageTk

class MainGUI:
    def __init__(self, master):
        self.master = master
        master.title("Integrated Hacking Toolbox")

        title_label = tk.Label(master, text="Select a tool to get started ", font=("Helvetica", 25, "bold"))
        title_label.grid(row=0, column=0, columnspan=1, pady=(10, 0), sticky="w")

        tool_data = [
            {"name": "Network Scanner Tool", "image_path": "network.png"},
            {"name": "Steganography Tool", "image_path": "steg.png"},
            {"name": "Keylogger Tool", "image_path": "keylog.jpeg"},
        ]

        self.selected_tool = tk.StringVar()

        self.radio_buttons = []
        self.image_references = []
        image_width = 100  
        image_height = 100
        for i, tool_info in enumerate(tool_data,start=1):
            tool_name = tool_info["name"]
            image_path = tool_info["image_path"]

            image = Image.open(image_path)
            
            original_image = Image.open(image_path)
            
            
            resized_image = original_image.resize((image_width, image_height), Image.ANTIALIAS)

            
            tk_image = ImageTk.PhotoImage(resized_image)

            
            self.image_references.append(tk_image)
            label = tk.Label(master, compound="left")
            label.image = tk_image  
            label.configure(image=tk_image)
            label.grid(row=i, column=1, pady=(5, 0), sticky="w")

            button = tk.Radiobutton(master, text=tool_name, variable=self.selected_tool, value=tool_name)
            button.grid(row=i, column=0, pady=(5, 0), sticky="w")
            self.radio_buttons.append(button)

   
        self.button_run = tk.Button(master, text="Run tool", command=self.run_selected_tool , fg="blue")
        self.button_run.grid(row=len(tool_data)+1, column=0,pady=10)


        text_line1 = tk.Label(master, text="       Designed & implemented by Neeraj , Raghav maheshwari and Varun Antwal", font=("Arial", 15, "bold"))
        text_line1.grid(row=9, column=0, columnspan=3, pady=(5, 0), sticky="w")

        self.button_quit = tk.Button(master, text="Quit", command=master.quit ,fg="red")
        self.button_quit.grid(row=len(tool_data)+5, column=0, pady=10)
        



        window_width = 600  
        window_height = 600 
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        master.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        master.columnconfigure(0, weight=3)

    def run_selected_tool(self):
      
        selected_tool = self.selected_tool.get()
        if selected_tool == "Network Scanner Tool":
            self.run_script("network.py")
        elif selected_tool == "Steganography Tool":
            self.run_script("steg.py")
        elif selected_tool == "Keylogger Tool":
            self.run_script("keylogger.py")

    def run_script(self, script_name):
       
        Popen([sys.executable, script_name])

if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()
