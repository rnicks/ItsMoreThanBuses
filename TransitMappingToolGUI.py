from Tkinter import *
from tkFileDialog import *

#TODO add check for OS (OSX, Windows, Linux) for file directory initial path

#GUI for transit mapping tool
class TransitMappingToolGUI:

    #constructor initializes main window
    def __init__(self, master):
        self.master = master
        master.title("A Simple Transit Mapping Tool")

        self.OSMFilePath = ""
        self.GTFSFilePath = ""
        self.OTPFilePath = ""
        self.timePeriodStart = 0000
        self.timePeriodEnd = 0000
        self.maxTravelTime = 0
        self.OS = "OSX"

        self.OSMLabel = Label(master, text="Select the map data (OSM file) for your desired service area:")
        self.OSMLabel.pack()

        self.OSMButton = Button(master, text="Select OSM", command=self.selectOSM)
        self.OSMButton.pack()

        self.GTFSLabel = Label(master, text="Select the GTFS data for your transit system:")
        self.GTFSLabel.pack()

        self.GTFSButton = Button(master, text="Select GTFS", command=self.selectGTFS)
        self.GTFSButton.pack()

        self.OTPLabel = Label(master, text="Select your OpenTripPlanner .jar file:")
        self.OTPLabel.pack()

        self.OTPButton = Button(master, text="Select jar file", command=self.selectOTP)
        self.OTPButton.pack()

        self.timeStartLabel = Label(master, text="Enter the start time for your time increment (e.g. 0700)")
        self.timeStartLabel.pack()

        self.timeEndLabel = Label(master, text="Enter the end time for your time increment (e.g. 0800)")
        self.timeEndLabel.pack()

        self.maxTravelTimeLabel = Label(master, text="Enter the maximum travel time in seconds:")
        self.maxTravelTimeLabel.pack()

        self.helpButton = Button(master, text="Help", command=self.helpMe)
        self.helpButton.pack()

    #Method to choose the OSM filepath
    def selectOSM(self):
        if self.OS == "OSX" or self.OS == "Linux":
            self.OSMFilePath = askopenfilename(initialdir = "/", title = "Select OSM File", filetypes=(("OSM Files", "*.PBF"), ("all files", "*.*")))
            print(self.OSMFilePath) #temporary print for testing

        elif self.OS == "Windows":
            self.OSMFilePath = askopenfilename(initialdir = "C:\\", title = "Select OSM File", filetypes=(("OSM Files", "*.PBF"), ("all files", "*.*")))
            print(self.OSMFilePath) #temporary print for testing

    #Method to choose the GTFS filepath
    def selectGTFS(self):
        if self.OS == "OSX" or self.OS == "Linux":
            self.GTFSFilePath = askopenfilename(initialdir = "/", title = "Select GTFS File", filetypes=(("GTFS Files", "*.zip"), ("all files", "*.*")))
            print(self.GTFSFilePath) #temporary print for testing

        elif self.OS == "Windows":
            self.GTFSFilePath = askopenfilename(initialdir = "C:\\", title = "Select GTFS File", filetypes=(("GTFS Files", "*.zip"), ("all files", "*.*")))
            print(self.GTFSFilePath) #temporary print for testing

    #Method to choose OTP.jar filepath
    def selectOTP(self):
        if self.OS == "OSX" or self.OS == "Linux":
            self.OTPFilePath = askopenfilename(initialdir = "/", title = "Select OpenTripPlanner jar", filetypes=(("jar files", "*.jar"), ("all files", "*.*")))
            print(self.OTPFilePath) #temporary print for testing
            
        elif self.OS == "Windows":
            self.OTPFilePath = askopenfilename(initialdir = "C:\\", title = "Select OpenTripPlanner jar", filetypes=(("jar Files", "*.jar"), ("all files", "*.*")))
            print(self.OTPFilePath) #temporary print for testing

    #Method to launch help page
    def helpMe(self):
        print("Help")
        #TODO add help functionality: button launches new window which displays explanation and instructions



    

root = Tk()
gui = TransitMappingToolGUI(root)
root.mainloop()
