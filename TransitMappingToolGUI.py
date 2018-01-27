from Tkinter import Tk, Label, Button

class TransitMappingToolGUI:
    def __init__(self, master):
        self.master = master
        master.title("A Simple Transit Mapping Tool")

        self.label = Label(master, text="Some test text")
        self.label.pack()

        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def greet(self):
            print("Greetings!")

root = Tk()
gui = TransitMappingToolGUI(root)
root.mainloop()
