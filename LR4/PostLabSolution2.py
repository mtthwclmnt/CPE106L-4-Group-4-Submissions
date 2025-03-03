#VANCE DAVID G. SAMIA
import tkinter as tk
from tkinter import filedialog

def open_text_file():
    root = tk.Tk()
    root.withdraw()  

    file_path = filedialog.askopenfilename(
        title="Select a Text File",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )

    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
            print("File Content:\n", content)

# Call the function to open the file dialog and read a file
open_text_file()
