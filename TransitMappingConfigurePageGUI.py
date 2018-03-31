from Tkinter import *
from tkFileDialog import *
import tkMessageBox
import os
import subprocess
from subprocess import check_output
import webbrowser
import psycopg2
import threading
from multiprocessing import Pool, TimeoutError

class TransitMappingConfigurePageGUI:

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

        self.analysisTypeVar = StringVar()
        self.precisionPointsVar = StringVar()
        self.dbName = ""
        self.dbUsername = ""
        self.dbPassword = ""
        self.analysisType = ""
        self.routerName = ""
        self.precisionPoints = ""
        self.gridSize = ""
        self.precisionPoints = ""
        self.gridFilePath = ""
        self.gridLabelText = StringVar()

        
##########################################################################################

        #create UI elements (buttons, text fields etc)

        self.dbUsernameLabel = Label(master, text="Enter the username for your PostgreSQL database:")
        self.dbUsernameLabel.grid(column=0, row =0)

        self.dbUsernameEntry = Entry(master)
        self.dbUsernameEntry.grid(column=1, row = 0)

        self.dbPasswordLabel = Label(master, text="Enter the password for your PostgreSQL database:")
        self.dbPasswordLabel.grid(column=0, row =1)

        self.dbPasswordEntry = Entry(master)
        self.dbPasswordEntry.grid(column=1, row = 1)

        self.dbNameLabel = Label(master, text="Enter the name of your PostgreSQL database:")
        self.dbNameLabel.grid(column=0, row = 2)

        self.dbNameEntry = Entry(master)
        self.dbNameEntry.grid(column=1, row = 2)

        self.dbUsernameLabel = Label(master, text="Select an analysis type (single GTFS file or pre/post analysis)")
        self.dbUsernameLabel.grid(column=0, row =3)

        self.GTFSButton1 = Radiobutton(master, text="Single Analysis", variable = self.analysisTypeVar, value="single")
        self.GTFSButton1.grid(column=0, row=4)

        self.GTFSButton2 = Radiobutton(master, text="Pre/Post Analysis", variable = self.analysisTypeVar, value="pre-post")
        self.GTFSButton2.grid(column=0, row=5)

        self.analysisTypeVar.set("single")

        self.routerNameLabel = Label(master, text="Enter a name for your OpenTripPlanner router:")
        self.routerNameLabel.grid(column=0, row =6)

        self.routerNameEntry = Entry(master)
        self.routerNameEntry.grid(column=1, row = 6)

        self.gridSizeLabel = Label(master, text="Enter the distance between gridpoints in meters (suggested: 500):")
        self.gridSizeLabel.grid(column=0, row =7)

        self.gridSizeEntry = Entry(master)
        self.gridSizeEntry.grid(column=1, row = 7)
        
        self.setupDBLabel = Label(master, text="Select the level of precision for latitude/longitude coordinates:")
        self.setupDBLabel.grid(column=0, row=8)

        self.precisionButton1 = Radiobutton(master, text="3 points of precision", variable = self.precisionPointsVar, value="3")
        self.precisionButton1.grid(column=0, row=9)

        self.precisionButton2 = Radiobutton(master, text="4 points of precision", variable = self.precisionPointsVar, value="4")
        self.precisionButton2.grid(column=0, row=10)

        self.precisionButton3 = Radiobutton(master, text="5 points of precision", variable = self.precisionPointsVar, value="5")
        self.precisionButton3.grid(column=0, row=11)

        self.precisionPointsVar.set("3")

        self.selectGridLabel = Label(master, text="Select existing point grid shapefile:")
        self.selectGridLabel.grid(column=0, row=12)

        self.selectGridButton = Button(master, text="Select Grid", command=self.selectGrid)
        self.selectGridButton.grid(column=1, row=12)

        self.gridPathLabel = Label(master, textvariable=self.gridLabelText, fg="blue")
        self.gridPathLabel.grid(column=0, row=13)

        self.setupDBButton = Button(master, text="Set up database", command=self.setupDB)
        self.setupDBButton.grid(column=0, row=14)

        self.setupDBLabel = Label(master, text="Creates database tables used by the program (only needs to be run once)")
        self.setupDBLabel.grid(column=0, row=15)

        self.configureButton = Button(master, text="Launch Tool", command=self.configure)
        self.configureButton.grid(column=1, row=14)


##########################################################################################

    def configure(self):

        self.dbUsername = self.dbUsernameEntry.get()
        self.dbPassword = self.dbPasswordEntry.get()
        self.dbName = self.dbNameEntry.get()
        self.analysisType = self.analysisTypeVar.get()
        self.routerName = self.routerNameEntry.get()
        self.gridSize = self.gridSizeEntry.get()
        self.precisionPoints = self.precisionPointsVar.get()

        if self.dbUsername == "" or self.dbPassword == "" or self.dbName == "":
            #Pop up error message
            tkMessageBox.showwarning("Error", "You must enter a database username, password, and database name")
            return
        if self.gridFilePath == "":
            tkMessageBox.showwarning("Error", "You must select a grid point shapefile.")
            return

        process1 = subprocess.Popen(["shp2pgsql", "-I", "-s 4326", self.gridFilePath, "gridpoints"], stdout=subprocess.PIPE)
        process2 = subprocess.Popen(["psql", "-U", self.dbUsername, "-d", self.dbName], stdin=process1.stdout)
            

    def selectGrid(self):
        if self.OS == "OSX" or self.OS == "Linux":
            self.gridFilePath = askopenfilename(initialdir = "/", title = "Select OSM File", filetypes=(("Shape Files", "*.shp"), ("all files", "*.*")))

        elif self.OS == "Windows":
            self.gridFilePath = askopenfilename(initialdir = "C:\\", title = "Select OSM File", filetypes=(("Shape Files", "*.shp"), ("all files", "*.*")))

        self.gridLabelText.set(self.gridFilePath) #display selected file path
        
 

    def setupDB(self):
        
        self.dbUsername = self.dbUsernameEntry.get()
        self.dbPassword = self.dbPasswordEntry.get()
        self.dbName = self.dbNameEntry.get()

        if self.dbUsername == "" or self.dbPassword == "" or self.dbName == "":
            #Pop up error message
            tkMessageBox.showwarning("Error", "You must enter a database username, password, and database name")
            return

        tables = (

            """CREATE EXTENSION IF NOT EXISTS postgis""",
            
            """ CREATE TABLE GridPoints(
            g_id INTEGER PRIMARY KEY,

            geom FLOAT(8),

            x FLOAT(8),

            y FLOAT(8),

            loc_id INTEGER)""",



            """ CREATE TABLE GridLocation(

            loc_id INTEGER PRIMARY KEY,

            name VARCHAR(50))""",



            """ CREATE TABLE Analysis(

            analysis_id INTEGER PRIMARY KEY,

            name VARCHAR(50),

            date DATE,

            loc_id INTEGER,

            FOREIGN KEY (loc_id) REFERENCES GridLocation(loc_id))""",



            """ CREATE TABLE AnalysisResults(

            g_id INTEGER,

            analysis_id INTEGER,

            typePre INTEGER,

            typePost INTEGER,

            overlap_count INTEGER,

            FOREIGN KEY (g_id) REFERENCES GridPoints(g_id))""",



            """ CREATE TABLE IsoChrones(

            Iso_ID INTEGER,

            analysis_id INTEGER,

            flag_Pre INTEGER,

            flag_Post INTEGER,

            FOREIGN KEY (analysis_id) REFERENCES Analysis(analysis_id))""",


            """ CREATE TABLE IsoTables(
            )                
            """)


        connString = "host='localhost' dbname='" + self.dbName + "' user='" + self.dbUsername + "' password='" + self.dbPassword + "'"


        dbConnection = psycopg2.connect(connString)
        dbCursor =  dbConnection.cursor()

        for table in tables:

            dbCursor.execute(table)

            dbConnection.commit()

 




#launch main window
root = Tk()
gui = TransitMappingConfigurePageGUI(root)
root.mainloop()
