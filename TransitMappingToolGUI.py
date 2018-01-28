from Tkinter import *
from tkFileDialog import *
import os
import subprocess
from subprocess import check_output
import webbrowser

#GUI for transit mapping tool
class TransitMappingToolGUI:

    #constructor initializes main window
    def __init__(self, master):
        self.master = master
        master.title("A Simple Transit Mapping Tool")

        #check system OS
        if os.name == 'posix':
            self.OS = "OSX"
        elif os.name == 'nt':
            self.OS = "Windows"
        else:
            self.OS = "OSX"

        #create object variables
        self.OSMFilePath = ""
        self.OSMLabelText = StringVar()
        self.GTFSFilePath = ""
        self.GTFSLabelText = StringVar()
        self.OTPFilePath = ""
        self.OTPLabelText = StringVar()
        self.OSMFilePathParent = ""
        self.timePeriodStart = 0000
        self.timePeriodEnd = 0000
        self.maxTravelTime = 0

        #create UI elements (buttons, text fields etc)
        self.OSMLabel = Label(master, text="Select the map data (OSM file) for your desired service area:")
        self.OSMLabel.grid(column=0, row=0)

        self.OSMLabelPath = Label(master, textvariable=self.OSMLabelText, fg="blue")
        self.OSMLabelPath.grid(column=0, row=1)

        self.OSMButton = Button(master, text="Select OSM", command=self.selectOSM)
        self.OSMButton.grid(column=1, row=0)

        self.GTFSLabel = Label(master, text="Select the GTFS data for your transit system:")
        self.GTFSLabel.grid(column=0, row=2)
        
        self.GTFSLabelPath = Label(master, textvariable=self.GTFSLabelText, fg="blue")
        self.GTFSLabelPath.grid(column=0, row=3)

        self.GTFSButton = Button(master, text="Select GTFS", command=self.selectGTFS)
        self.GTFSButton.grid(column=1, row=2)

        self.OTPLabel = Label(master, text="Select your OpenTripPlanner .jar file:")
        self.OTPLabel.grid(column=0, row=5)

        self.OTPLabelPath = Label(master, textvariable=self.OTPLabelText, fg="blue")
        self.OTPLabelPath.grid(column=0, row=6)

        self.OTPButton = Button(master, text="Select jar file", command=self.selectOTP)
        self.OTPButton.grid(column=1, row=5)

        self.timeStartLabel = Label(master, text="Enter the start time for your time increment (e.g. 0700)")
        self.timeStartLabel.grid(column=0, row=7)

        self.timeStartEntry = Entry(master)
        self.timeStartEntry.grid(column=0, row=8)

        self.timeStartButton = Button(master, text="Set", command=self.setStart)
        self.timeStartButton.grid(column=1,row=8)

        self.timeEndLabel = Label(master, text="Enter the end time for your time increment (e.g. 0800)")
        self.timeEndLabel.grid(column=0, row=9)

        self.timeEndEntry = Entry(master)
        self.timeEndEntry.grid(column=0, row=10)

        self.timeEndButton = Button(master, text="Set", command=self.setEnd)
        self.timeEndButton.grid(column=1, row=10)

        self.maxTravelTimeLabel = Label(master, text="Enter the maximum travel time in seconds:")
        self.maxTravelTimeLabel.grid(column=0, row=11)

        self.maxTravelTimeEntry = Entry()
        self.maxTravelTimeEntry.grid(column=0, row=12)

        self.travelTimeButton = Button(master, text="Set", command=self.setTravelTime)
        self.travelTimeButton.grid(column=1, row=12)

        self.launchOTPButton = Button(master, text="Launch OpenTripPlanner", command=self.launchOTP)
        self.launchOTPButton.grid(column=0, row=14)

        self.generateGridButton = Button(master, text="Generate Point Grid", command=self.generateGrid)
        self.generateGridButton.grid(column=1, row=14)

        self.helpButton = Button(master, text="Help", command=self.helpMe)
        self.helpButton.grid(column=0, row=15)

        #end of UI elements

    #Method to choose the OSM filepath
    def selectOSM(self):
        if self.OS == "OSX" or self.OS == "Linux":
            self.OSMFilePath = askopenfilename(initialdir = "/", title = "Select OSM File", filetypes=(("OSM Files", "*.PBF"), ("all files", "*.*")))

        elif self.OS == "Windows":
            self.OSMFilePath = askopenfilename(initialdir = "C:\\", title = "Select OSM File", filetypes=(("OSM Files", "*.PBF"), ("all files", "*.*")))
            
        self.OSMLabelText.set(self.OSMFilePath) #display selected file path
        self.OSMFilePathParent = os.path.dirname(self.OSMFilePath) #set directory path for folder containing OSM and GTFS files

    #Method to choose the GTFS filepath
    def selectGTFS(self):
        if self.OS == "OSX" or self.OS == "Linux":
            self.GTFSFilePath = askopenfilename(initialdir = "/", title = "Select GTFS File", filetypes=(("GTFS Files", "*.zip"), ("all files", "*.*")))

        elif self.OS == "Windows":
            self.GTFSFilePath = askopenfilename(initialdir = "C:\\", title = "Select GTFS File", filetypes=(("GTFS Files", "*.zip"), ("all files", "*.*")))

        self.GTFSLabelText.set(self.GTFSFilePath) #display selected file path

    #Method to choose OTP.jar filepath
    def selectOTP(self):
        if self.OS == "OSX" or self.OS == "Linux":
            self.OTPFilePath = askopenfilename(initialdir = "/", title = "Select OpenTripPlanner jar", filetypes=(("jar files", "*.jar"), ("all files", "*.*")))
            
        elif self.OS == "Windows":
            self.OTPFilePath = askopenfilename(initialdir = "C:\\", title = "Select OpenTripPlanner jar", filetypes=(("jar Files", "*.jar"), ("all files", "*.*")))

        self.OTPLabelText.set(self.OTPFilePath) #display selected file path

    #method to set the start of the desired time increment
    def setStart(self):
        self.timePeriodStart = self.timeStartEntry.get()
        print(self.timePeriodStart)

    #method to set the end of the desired time increment
    def setEnd(self):
        self.timePeriodEnd = self.timeEndEntry.get()
        print(self.timePeriodEnd)

    #method to set the maximum allowable travel time
    def setTravelTime(self):
        self.maxTravelTime = self.maxTravelTimeEntry.get()
        print(self.maxTravelTime)

    #method to launch OpenTripPlanner based on specified file paths
    #TODO figure out a way of printing confirmation once OTP is open
    #TODO figure out way of saving graph to disk in folder named after router (eg halifax)
    #maybe user configurable (textbox for 'name of router' or similar?)
    def launchOTP(self):
        
        subprocess.Popen(['java', '-Xmx4G', '-jar', self.OTPFilePath, '--build', self.OSMFilePathParent, '--inMemory', '--analyst'])

        #first create graph file on disk
        #subprocess.call(['java', '-Xmx4g', '-jar', self.OTPFilePath, '--build', self.OSMFilePathParent])

        #once graph is built, launch router
        #subprocess.Popen(['java', '-Xmx4G', '-jar', self.OTPFilePath, '--basepath', self.OSMFilePathParent, '--router', 'halifax', '--analyst', '--server'])

        #once router is running, launch webbrowser
        #this might not be needed, but for now can be confirmation that OTP is running properly
        #webbrowser.open('localhost:8080')

    #method to launch a script to generate a regular point grid using QGIS
    def generateGrid(self):
        print("This will eventually generate a point grid in QGIS")

    #Method to launch help page
    def helpMe(self):
        print("This will eventually launch a help menu")
        #TODO add help functionality: button launches new window which displays explanation and instructions


#launch main window
root = Tk()
gui = TransitMappingToolGUI(root)
root.mainloop()
