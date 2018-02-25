from Tkinter import *
from tkFileDialog import *
import os
import subprocess
from subprocess import check_output
import webbrowser

class TransitMappingConfigurePageGUI:

    def __init__(self, master):
        self.master = master
        master.title("A Simple Transit Mapping Tool"
        




#launch main window
root = Tk()
gui = TransitMappingToolGUI(root)
root.mainloop()
