# main.py
import tkinter as tk
from app import AnnotationApp

if __name__ == "__main__":
    root = tk.Tk()
    app = AnnotationApp(root)
    root.mainloop()