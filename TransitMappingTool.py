from Tkinter import *
from tkFileDialog import *
import os
import subprocess
from subprocess import check_output
import webbrowser
import urllib, json, urllib2
import psycopg2
import sys
from datetime import datetime
from datetime import timedelta
import tkMessageBox

dbName = ""
dbUsername = ""
dbPassword = ""
analysisType = ""
routerName = ""
precisionPoints = ""
gridSize = ""
gridFilePath = ""
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
        
        #update object variables (global) 
        global analysisType  
        global precisionPoints
        global gridFilePath    
        #create object variables (local)
        self.analysisTypeVar = StringVar()
        self.precisionPointsVar = StringVar()
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
        
        self.setupDBLabel = Label(master, text="Select the level of precision for latitude/longitude coordinates:")
        self.setupDBLabel.grid(column=0, row=8)

        self.precisionButton1 = Radiobutton(master, text="3 points of precision", variable = self.precisionPointsVar, value="3")
        self.precisionButton1.grid(column=0, row=9)

        self.precisionButton2 = Radiobutton(master, text="4 points of precision", variable = self.precisionPointsVar, value="4")
        self.precisionButton2.grid(column=0, row=10)

        self.precisionButton3 = Radiobutton(master, text="5 points of precision", variable = self.precisionPointsVar, value="5")
        self.precisionButton3.grid(column=0, row=11)

        self.precisionPointsVar.set("3")

        self.gridPointsLabel = Label (master, text ="Select the point grid shapefile: ")
        self.gridPointsLabel.grid(column=0, row = 12)

        self.gridPointsButton = Button (master, text="Select grid", command=self.selectGrid)
        self.gridPointsButton.grid(column=1, row = 12)

        self.gridLabelPath = Label(master, textvariable=self.gridLabelText, fg="blue")
        self.gridLabelPath.grid(column=0, row=13)
        
        self.setupDBButton = Button(master, text="Set up database", command=self.setupDB)
        self.setupDBButton.grid(column=0, row=14)

        self.setupDBLabel = Label(master, text="Creates database tables used by the program (only needs to be run once)")
        self.setupDBLabel.grid(column=0, row=15)

        self.configureButton = Button(master, text="Configure and Launch", command=self.configure)
        self.configureButton.grid(column=1, row=14)


##########################################################################################

    def selectGrid(self):
        try:
            global gridFilePath
            if self.OS == "OSX" or self.OS == "Linux":
                gridFilePath = askopenfilename(initialdir = "/", title = "Select Shape File", filetypes=(("SHP Files", "*.shp"), ("all files", "*.*")))
    
            elif self.OS == "Windows":
                gridFilePath = askopenfilename(initialdir = "C:\\", title = "Select Shape File", filetypes=(("SHP Files", "*.shp"), ("all files", "*.*")))
    
            self.gridLabelText.set(gridFilePath) #display selected file path
        except NameError:
            print "please select a file"
        
#Note: -Configure and Launch will launch multiple windows, only press once,
#      -Configure and Launch page needs to remain open 
    def configure(self):
        global dbName 
        global dbUsername 
        global dbPassword 
        global analysisType 
        global routerName 
        global gridSize 
        global precisionPoints
        dbUsername = self.dbUsernameEntry.get()
        dbPassword = self.dbPasswordEntry.get()
        dbName = self.dbNameEntry.get()
        analysisType = self.analysisTypeVar.get()
        precisionPoints = self.precisionPointsVar.get()

        if dbUsername == "" or dbPassword == "" or dbName == "":
            #Pop up error message
            tkMessageBox.showwarning("Error", "You must enter a database username, password, and database name")
            return


        connString = "host='localhost' dbname='" + dbName + "' user='" + dbUsername + "' password='" + dbPassword + "'"

        dbConnection = psycopg2.connect(connString)
        dbCursor =  dbConnection.cursor()

        #clear gridpoints table
        dbCursor.execute("TRUNCATE gridpoints RESTART IDENTITY CASCADE")
        dbConnection.commit()

        p1 = subprocess.Popen(['shp2pgsql', '-a', '-I', '-s','4326', gridFilePath, 'gridpoints'], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(['psql', '-d', dbName, '-U', dbUsername], stdin=p1.stdout)
        print p2.communicate()

         #initialize pre, post, and diff columns
        dbCursor.execute("UPDATE gridpoints SET preanalysis = 0, postanalysis = 0, diff = 0")
        dbConnection.commit()
        
        self.newWindow = Toplevel(root)
        self.app = TransitMappingToolGUI(self.newWindow)
        
    def setupDB(self):
        global dbName 
        global dbUsername 
        global dbPassword        
        dbUsername = self.dbUsernameEntry.get()
        dbPassword = self.dbPasswordEntry.get()
        dbName = self.dbNameEntry.get()

        if dbUsername == "" or dbPassword == "" or dbName == "":
            #Pop up error message
            tkMessageBox.showwarning("Error", "You must enter a database username, password, and database name")
            return

        tables = (
            """CREATE EXTENSION IF NOT EXISTS postgis""",

            """ CREATE TABLE IF NOT EXISTS gridpoints(

            gid SERIAL PRIMARY KEY,

            id SERIAL,

            geom geometry,

            preAnalysis INTEGER DEFAULT 0,

            postAnalysis INTEGER DEFAULT 0,

            diff INTEGER DEFAULT 0)""",
            

            """ CREATE TABLE IF NOT EXISTS GridLocation(

            loc_id INTEGER PRIMARY KEY,

            name VARCHAR(50))""",



            """ CREATE TABLE IF NOT EXISTS Analysis(

            analysis_id INTEGER PRIMARY KEY,

            name VARCHAR(50),

            date DATE,

            loc_id INTEGER,

            FOREIGN KEY (loc_id) REFERENCES GridLocation(loc_id))""",



            """ CREATE TABLE IF NOT EXISTS AnalysisResults(
            gid INTEGER,
            analysis_id INTEGER,
            preFlag BOOLEAN DEFAULT false,
            postFlag BOOLEAN DEFAULT false,
            diffFlag BOOLEAN DEFAULT false,
            overlap_count INTEGER)""",

             """ CREATE TABLE IF NOT EXISTS IsoChrones1(

             ogc_fid SERIAL,

             wkb_geometry geometry,

             time int,)""",


            """ CREATE TABLE IF NOT EXISTS IsoChrones2(

             ogc_fid SERIAL,

             wkb_geometry geometry,

             time int,)""",)


        connString = "host='localhost' dbname='" + dbName + "' user='" + dbUsername + "' password='" + dbPassword + "'"


        dbConnection = psycopg2.connect(connString)
        dbCursor =  dbConnection.cursor()

        for table in tables:

            dbCursor.execute(table)

            dbConnection.commit()
# #################################################end

#GUI for transit mapping tool
class TransitMappingToolGUI():

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
        #create object variables (local)
        self.OSMFilePath = ""
        self.OSMLabelText = StringVar()
        self.GTFSFilePath = ""
        self.GTFSLabelText = StringVar()
        self.OTPFilePath = ""
        self.GTFSLabelTextCompare = StringVar()
        self.OTPFilePathCompare = ""        
        self.OTPLabelText = StringVar()
        self.OSMFilePathParent = ""
        self.startDate = ""
        self.endDate = ""
        self.startTime = 0000
        self.endTime = 0000
        self.maxTravelTime = 0   #this is provided by user in minutes, but converted to seconds

        #this is a string containing the database credentials. for now it is hard coded, later on this will be drawn from user input
        self.connString = "host='localhost' dbname='test' user='robertnickerson' password='velcro'"
        self.dbname = "test"
        self.dbuser = "robertnickerson"
        self.dbpassword = "velcro"


# #########################################################################################

        #create UI elements (buttons, text fields etc)
        self.OSMLabel = Label(master, text="Select the map data (OSM file) for your desired service area:")
        self.OSMLabel.grid(column=0, row=0)

        self.OSMLabelPath = Label(master, textvariable=self.OSMLabelText, fg="blue")
        self.OSMLabelPath.grid(column=0, row=1)

        self.OSMButton = Button(master, text="Select OSM", command=self.selectOSM)
        self.OSMButton.grid(column=1, row=0)
        
        #original GTFS button
        self.GTFSLabel = Label(master, text="Select the GTFS data for your transit system:")
        self.GTFSLabel.grid(column=0, row=2)

        self.GTFSLabelPath = Label(master, textvariable=self.GTFSLabelText, fg="blue")
        self.GTFSLabelPath.grid(column=0, row=3)

        self.GTFSButton = Button(master, text="Select GTFS", command=self.selectGTFS)
        self.GTFSButton.grid(column=1, row=2)
        #GTFS compare 
        if analysisType == "pre-post":
            self.GTFSLabelCompare = Label(master, text="Select the GTFS data for your transit system that you want to compare:")
            self.GTFSLabelCompare.grid(column=0, row=4)
            
            self.GTFSLabelPathCompare = Label(master, textvariable=self.GTFSLabelTextCompare, fg="blue")
            self.GTFSLabelPathCompare.grid(column=0, row=5)
        
            self.GTFSButtonCompare = Button(master, text="Select GTFS", command=self.selectGTFSCompare)
            self.GTFSButtonCompare.grid(column=1, row=4)        

        self.OTPLabel = Label(master, text="Select your OpenTripPlanner .jar file:")
        self.OTPLabel.grid(column=0, row=7)

        self.OTPLabelPath = Label(master, textvariable=self.OTPLabelText, fg="blue")
        self.OTPLabelPath.grid(column=0, row=8)

        self.OTPButton = Button(master, text="Select jar file", command=self.selectOTP)
        self.OTPButton.grid(column=1, row=7)

        self.startDateLabel = Label(master, text="Enter the start date for your analysis (YYYY/MM/DD)")
        self.startDateLabel.grid(column=0, row=9)

        self.startDateEntry = Entry(master)
        self.startDateEntry.grid(column=0, row=10)

        self.endDateLabel = Label(master, text="Enter the end date for your analysis (YYYY/MM/DD)")
        self.endDateLabel.grid(column=0, row=11)

        self.endDateEntry = Entry(master)
        self.endDateEntry.grid(column=0, row=12)

        self.timeStartLabel = Label(master, text="Enter the start time for your time increment (hh:mm:ss)")
        self.timeStartLabel.grid(column=0, row=13)

        self.timeStartEntry = Entry(master)
        self.timeStartEntry.grid(column=0, row=14)


        self.timeEndLabel = Label(master, text="Enter the end time for your time increment (hh:mm:ss)")
        self.timeEndLabel.grid(column=0, row=15)

        self.timeEndEntry = Entry(master)
        self.timeEndEntry.grid(column=0, row=16)


        self.maxTravelTimeLabel = Label(master, text="Enter the target travel time in minutes:")
        self.maxTravelTimeLabel.grid(column=0, row=17)

        self.maxTravelTimeEntry = Entry(master)
        self.maxTravelTimeEntry.grid(column=0, row=18)


        self.launchOTPButton = Button(master, text="Launch OpenTripPlanner", command=self.launchOTP)
        self.launchOTPButton.grid(column=0, row=19)


        self.generateGridButton = Button(master, text="Generate Isochrones", command=self.generateIsochrones)
        self.generateGridButton.grid(column=0, row=20)

        self.helpButton = Button(master, text="Calculate Overlap", command=self.calculateOverlap)
        self.helpButton.grid(column=1, row=20)

        #end of UI elements

#Methods to get data from input fields
# ############################################################################################

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
        
    #Method to choose the GTFS compare filepath
    def selectGTFSCompare(self):
        if self.OS == "OSX" or self.OS == "Linux":
            self.GTFSFilePathCompare = askopenfilename(initialdir = "/", title = "Select GTFS File", filetypes=(("GTFS Files", "*.zip"), ("all files", "*.*")))

        elif self.OS == "Windows":
            self.GTFSFilePathCompare = askopenfilename(initialdir = "C:\\", title = "Select GTFS File", filetypes=(("GTFS Files", "*.zip"), ("all files", "*.*")))

        self.GTFSLabelTextCompare.set(self.GTFSFilePathCompare) #display selected file path    

    #Method to choose OTP.jar filepath
    def selectOTP(self):
        if self.OS == "OSX" or self.OS == "Linux":
            self.OTPFilePath = askopenfilename(initialdir = "/", title = "Select OpenTripPlanner jar", filetypes=(("jar files", "*.jar"), ("all files", "*.*")))

        elif self.OS == "Windows":
            self.OTPFilePath = askopenfilename(initialdir = "C:\\", title = "Select OpenTripPlanner jar", filetypes=(("jar Files", "*.jar"), ("all files", "*.*")))

        self.OTPLabelText.set(self.OTPFilePath) #display selected file path

    #Method to set the start date for the analysis
    def setStartDate(self):
        try:
            self.startDate = self.startDateEntry.get()
            print(self.startDate)
        except ValueError:
            print ("You need to enter valid time data in the start date field")



    #Method to set the start date for the analysis
    def setEndDate(self):
        try:
            self.endDate = self.endDateEntry.get()
            print(self.endDate)
        except ValueError:
            print "You need to enter valid time data end date field"


    #method to set the start of the desired time increment in datetime format
    def setStart(self):
        try:
            self.startTime = self.timeStartEntry.get()
            #convert input to a datetime object
            self.startTime = datetime.strptime(self.startTime, '%H:%M:%S')
            print(self.startTime.time())
            
        except ValueError:
            print "You need to enter valid time data in the start time field" 


    #method to set the end of the desired time increment in datetime format
    def setEnd(self):
        try:
            self.endTime = self.timeEndEntry.get()
            #convert input to datetime format
            self.endTime = datetime.strptime(self.endTime, '%H:%M:%S')
            print(self.endTime.time())
        except ValueError:
            print "You need to enter valid time data in the end time field"


    #method to set the maximum allowable travel time. Take input in minutes, convert to seconds
    def setTravelTime(self):
        try:
            self.maxTravelTime = self.maxTravelTimeEntry.get()
            self.maxTravelTime = int(self.maxTravelTime)
            self.maxTravelTime *= 60
            print(self.maxTravelTime)
        except ValueError:
            print "You need to enter valid number of minutes in the travel time field"


#Methods to perform actions
# ############################################################################################

    #method to launch OpenTripPlanner based on specified file paths
    #TODO figure out a way of printing confirmation once OTP is open
    #TODO figure out way of saving graph to disk in folder named after router (eg halifax)
    #maybe user configurable (textbox for 'name of router' or similar?)
    def launchOTP(self):

        self.setStartDate()
        self.setEndDate()
        self.setStart()
        self.setEnd()
        self.setTravelTime()

        #currently launches OTP in RAM, this is temporary til directory structuring is figured out
        subprocess.Popen(['java', '-Xmx4G', '-jar', self.OTPFilePath, '--build', self.OSMFilePathParent, '--inMemory', '--analyst'])

        #first create graph file on disk
        #subprocess.call(['java', '-Xmx4g', '-jar', self.OTPFilePath, '--build', self.OSMFilePathParent])

        #once graph is built, launch router
        #subprocess.Popen(['java', '-Xmx4G', '-jar', self.OTPFilePath, '--basepath', self.OSMFilePathParent, '--router', 'halifax', '--analyst', '--server'])

        #once router is running, launch OTP in browser
        #this won't be needed, but for now can be confirmation that OTP is running properly
        #webbrowser.open('localhost:8080')

    

    #method to generate URLs based on user input data, then grab isochrones from the address and insert into database
    def generateIsochrones(self):

        self.setStartDate()
        self.setEndDate()
        self.setStart()
        self.setEnd()
        self.setTravelTime()
        tempDirectory = self.OSMFilePathParent

        #try connecting to the database
        try:
            conn = psycopg2.connect(self.connString)
        except:
            print("Database connection error")

        #create a cursor, which is used to query the DB
        dbCursor = conn.cursor()

        #select all rows from table gridpoints in DB
        dbCursor.execute("""SELECT ST_X(geom), ST_Y(geom) from gridpoints""")

        #create a list to store the returned rows. Each row contains info on one gridpoint
        gridpoints = dbCursor.fetchall()

        timeIncrement = 5 #5 minute increments

        #TODO look into optimizing string concatenation for generating the URLs: it's inefficient in Java, is Python the same?

        def generate(gridpoints, prepost):
            #outer loop: for each point in gridpoints
            count = 0

            for point in gridpoints:
                #get x and y coords from each gridpoint
                #NOTE: in URL, order is (y,x) rather than (x,y), per Ben's example URL
                #truncate to 8 decimal places
                x = ""
                y = ""
                if precisionPoints == "3":
                  x = '%.3f'%(point[0])
                  y = '%.3f'%(point[1])

                elif precisionPoints == "4":
                  x = '%.4f'%(point[0])
                  y = '%.4f'%(point[1])

                elif precisionPoints == "5":
                  x = '%.5f'%(point[0])
                  y = '%.5f'%(point[1])

                #reset cursor to the beginning of the desired time increment
                timeCursor = self.startTime
                
                #inner loop: for each 5 minute increment in time period:
                while timeCursor <= self.endTime:
                    if prepost == "pre":
                        url = "http://localhost:8080/otp/routers/default/isochrone?&fromPlace=" + str(y) +"," + str(x) +"&date=" + str(self.startDate) + "&time="+ str(timeCursor.time()) + "&mode=WALK,TRANSIT&cutoffSec=" + str(self.maxTravelTime)
                    else:
                        url = "http://localhost:8080/otp/routers/default/isochrone?&fromPlace=" + str(y) +"," + str(x) +"&date=" + str(self.endDate) + "&time="+ str(timeCursor.time()) + "&mode=WALK,TRANSIT&cutoffSec=" + str(self.maxTravelTime)
                    print(str(count) + "-----" + url)
                    count += 1
                    
                    #request data from URL

                    try:
                        response = urllib2.urlopen(url)
                        
                    except urllib2.HTTPError as err:
                        timeCursor += timedelta(minutes = timeIncrement)
                        continue
                    except:
                        timeCursor += timedelta(minutes = timeIncrement)
                        continue

                    #parse the response as json
                    isochrone = json.load(response)

                    #write json to a tempfile, hopefully we can eliminate this step
                    with open(tempDirectory + "tempiso.json", "w") as f:
                        json.dump(isochrone, f)
                        
                    #insert temp json file into db
                    #decide whether to append or not: add "-append", to the subprocess command if so
                    if prepost == "pre":
                        subprocess.Popen(["ogr2ogr", "-f", "PostgreSQL", "PG:dbname="+ self.dbname + " user=" + self.dbuser + " password=" +self.dbpassword, "-nln","isochrones1", "-append", tempDirectory+ "tempiso.json"])
                    else:
                        subprocess.Popen(["ogr2ogr", "-f", "PostgreSQL", "PG:dbname="+ self.dbname + " user=" + self.dbuser + " password=" +self.dbpassword, "-nln","isochrones2", "-append", tempDirectory+ "tempiso.json"])
                        
                    #increment cursor by time increment (5 mins)
                    timeCursor += timedelta(minutes = timeIncrement)

        generate(gridpoints, "pre")
        
        if analysisType == "pre-post":
            generate(gridpoints, "post")

    #calculate the isochrone overlap values for pre analysis, post analysis, and the difference between the two
    def calculateOverlap(self):

    
   
        
        self.calculatePreOverlap()
        self.calculatePostOverlap()
        self.calculateOverlapDiff()

    #calculate the overlap values for the first version of the network
    def calculatePreOverlap(self):

        # Connect to the database

        connString = "host='localhost' dbname='" + dbName + "' user='" + dbUsername + "' password='" + dbPassword + "'"

        try:
            dbConnection = psycopg2.connect(self.connString)
        except:
            print("Database connection error")

        # Make the cursor

        dbCursor = dbConnection.cursor()

        dbCursor.execute("""UPDATE gridpoints SET preanalysis = preanalysis + total
                       FROM (SELECT gridpoints.gid, count(gridpoints.geom) AS total
                       FROM isochrones1 LEFT JOIN gridpoints
                       ON ST_Intersects(isochrones1.wkb_geometry, gridpoints.geom)
                       GROUP BY gridpoints.gid)
                       AS a WHERE gridpoints.gid = a.gid""")
        dbConnection.commit()

        dbCursor.execute("""INSERT INTO analysisresults (gid, analysis_id, preflag, overlap_count, geom)
                        select gid, 1, true, preanalysis as overlap_count, geom from gridpoints""")
        dbConnection.commit()

    #calculate the overlap values for the second version of the network
    def calculatePostOverlap(self):

        # Connect to the database

        connString = "host='localhost' dbname='" + dbName + "' user='" + dbUsername + "' password='" + dbPassword + "'"

        try:
            dbConnection = psycopg2.connect(self.connString)
        except:
            print("Database connection error")

        # Make the cursor

        dbCursor = dbConnection.cursor()

        dbCursor.execute("""UPDATE gridpoints SET postanalysis = postanalysis + total
                       FROM (SELECT gridpoints.gid, count(gridpoints.geom) AS total
                       FROM isochrones2 LEFT JOIN gridpoints
                       ON ST_Intersects(isochrones2.wkb_geometry, gridpoints.geom)
                       GROUP BY gridpoints.gid)
                       AS a WHERE gridpoints.gid = a.gid""")
        dbConnection.commit()

        dbCursor.execute("""INSERT INTO analysisresults (gid, analysis_id, postflag, overlap_count)
                        select gid, 1, true, preanalysis as overlap_count, geom from gridpoints""")

        dbConnection.commit()

    #calculate the difference in overlap values between versions of the network
    def calculateOverlapDiff(self):

        # Connect to the database

        connString = "host='localhost' dbname='" + dbName + "' user='" + dbUsername + "' password='" + dbPassword + "'"

        try:
            dbConnection = psycopg2.connect(self.connString)
        except:
            print("Database connection error")

        # Make the cursor

        dbCursor = dbConnection.cursor()

        dbCursor.execute("UPDATE gridpoints SET diff = preanalysis - postanalysis")
        dbConnection.commit()

        dbCursor.execute("""INSERT INTO analysisresults (gid, analysis_id, diffflag, overlap_count)
                        select gid, 1, true, preanalysis as overlap_count, geom from gridpoints""")

        dbConnection.commit()


    
    #Method to launch help page
    def helpMe(self):
        print("open help file")#throw in subprocess to open readme.txt

#End of Class
# ############################################################################################
#launch main window
root = Tk()
gui = TransitMappingConfigurePageGUI(root)
root.mainloop()

