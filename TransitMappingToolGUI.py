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
from pathos import pools
from pathos.helpers import freeze_support


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


##########################################################################################

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

        self.startDateLabel = Label(master, text="Enter the start date for your analysis (YYYY/MM/DD)")
        self.startDateLabel.grid(column=0, row=7)

        self.startDateButton = Button(master, text="Set", command=self.setStartDate)
        self.startDateButton.grid(column=1,row=8)

        self.startDateEntry = Entry(master)
        self.startDateEntry.grid(column=0, row=8)

        self.endDateLabel = Label(master, text="Enter the end date for your analysis (YYYY/MM/DD)")
        self.endDateLabel.grid(column=0, row=9)

        self.endDateButton = Button(master, text="Set", command=self.setEndDate)
        self.endDateButton.grid(column=1,row=10)

        self.endDateEntry = Entry(master)
        self.endDateEntry.grid(column=0, row=10)

        self.timeStartLabel = Label(master, text="Enter the start time for your time increment (hh:mm:ss)")
        self.timeStartLabel.grid(column=0, row=11)

        self.timeStartEntry = Entry(master)
        self.timeStartEntry.grid(column=0, row=12)

        self.timeStartButton = Button(master, text="Set", command=self.setStart)
        self.timeStartButton.grid(column=1,row=12)

        self.timeEndLabel = Label(master, text="Enter the end time for your time increment (hh:mm:ss)")
        self.timeEndLabel.grid(column=0, row=13)

        self.timeEndEntry = Entry(master)
        self.timeEndEntry.grid(column=0, row=14)

        self.timeEndButton = Button(master, text="Set", command=self.setEnd)
        self.timeEndButton.grid(column=1, row=14)

        self.maxTravelTimeLabel = Label(master, text="Enter the target travel time in minutes:")
        self.maxTravelTimeLabel.grid(column=0, row=15)

        self.maxTravelTimeEntry = Entry()
        self.maxTravelTimeEntry.grid(column=0, row=16)

        self.travelTimeButton = Button(master, text="Set", command=self.setTravelTime)
        self.travelTimeButton.grid(column=1, row=16)

        self.launchOTPButton = Button(master, text="Launch OpenTripPlanner", command=self.launchOTP)
        self.launchOTPButton.grid(column=0, row=17)

        self.generateGridButton = Button(master, text="Generate Point Grid", command=self.generateGrid)
        self.generateGridButton.grid(column=1, row=17)

        self.generateGridButton = Button(master, text="Generate Isochrones", command=self.generateIsochrones)
        self.generateGridButton.grid(column=0, row=18)

        self.helpButton = Button(master, text="Help", command=self.helpMe)
        self.helpButton.grid(column=1, row=18)

        #end of UI elements

#Methods to get data from input fields
#############################################################################################

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

    #Method to set the start date for the analysis
    def setStartDate(self):
        self.startDate = self.startDateEntry.get()
        print(self.startDate)

    #Method to set the start date for the analysis
    def setEndDate(self):
        self.endDate = self.endDateEntry.get()
        print(self.endDate)

    #method to set the start of the desired time increment in datetime format
    def setStart(self):
        self.startTime = self.timeStartEntry.get()
        #convert input to a datetime object
        self.startTime = datetime.strptime(self.startTime, '%H:%M:%S')
        print(self.startTime.time())

    #method to set the end of the desired time increment in datetime format
    def setEnd(self):
        self.endTime = self.timeEndEntry.get()
        #convert input to datetime format
        self.endTime = datetime.strptime(self.endTime, '%H:%M:%S')
        print(self.endTime.time())

    #method to set the maximum allowable travel time. Take input in minutes, convert to seconds
    def setTravelTime(self):
        self.maxTravelTime = self.maxTravelTimeEntry.get()
        self.maxTravelTime = int(self.maxTravelTime)
        self.maxTravelTime *= 60
        print(self.maxTravelTime)

#Methods to perform actions
#############################################################################################

    #method to launch OpenTripPlanner based on specified file paths
    #TODO figure out a way of printing confirmation once OTP is open
    #TODO figure out way of saving graph to disk in folder named after router (eg halifax)
    #maybe user configurable (textbox for 'name of router' or similar?)
    def launchOTP(self):

        #currently launches OTP in RAM, this is temporary til directory structuring is figured out
        subprocess.Popen(['java', '-Xmx4G', '-jar', self.OTPFilePath, '--build', self.OSMFilePathParent, '--inMemory', '--analyst'])

        #first create graph file on disk
        #subprocess.call(['java', '-Xmx4g', '-jar', self.OTPFilePath, '--build', self.OSMFilePathParent])

        #once graph is built, launch router
        #subprocess.Popen(['java', '-Xmx4G', '-jar', self.OTPFilePath, '--basepath', self.OSMFilePathParent, '--router', 'halifax', '--analyst', '--server'])

        #once router is running, launch OTP in browser
        #this won't be needed, but for now can be confirmation that OTP is running properly
        #webbrowser.open('localhost:8080')

    #method to launch a script to generate a regular point grid using postGIS
    def generateGrid(self):

        #try connecting to the database
        try:
            conn = psycopg2.connect(self.connString)
        except:
            print("Database connection error")

        #
        #function to create point grid, takes in a geo polygon column from nov27post.
        #dividing/multiplying all values in order to adapt to smaller latitude/longitude points
        #Using st_setsrid, this function im not totaly sure is nessary given data being inputed
        #Work Cited: https://gis.stackexchange.com/questions/4663/how-to-create-regular-point-grid-inside-a-polygon-in-postgis
        #


        #create a cursor, which is used to query the DB
        dbCursor = conn.cursor()

        #####
        
        #Select map extent as geom from OSM file (after importing OSM to postGIS)
        

        #####

        #create function
        dbCursor.execute("""
        CREATE OR REPLACE FUNCTION makegrid(geometry, integer, integer)
        RETURNS geometry AS
        '
        SELECT ST_Collect(st_setsrid(ST_POINT(x/$3::float,y/$3::float),st_srid($1))) FROM 
          generate_series(
                        (round(floor(st_xmin($1)*$3)::int/$2)*$2)::int, 
                        (round(ceiling(st_xmax($1)*$3)::int/$2)*$2)::int,
                        $2) as x ,
          generate_series(
                        (round(floor(st_ymin($1)*$3)::int/$2)*$2)::int, 
                        (round(ceiling(st_ymax($1)*$3)::int/$2)*$2)::int,
                        $2) as y 
        WHERE st_intersects($1,ST_SetSRID(ST_POINT(x/$3::float,y/$3::float),ST_SRID($1)))
        '

        LANGUAGE sql""")

        #
        #SELECT statement to access function uses nov27post as input table and the geom column as polygon, third integer is scale
 
        #execute function
        dbCursor.execute("""
            
        SELECT makegrid (bextent, 1000, 10000) into gridpointtest FROM
            (SELECT ST_SetSRID(ST_Extent(way),4326) as bextent FROM planet_osm_polygon) as grid
;""")
        conn.commit()
        #TODO insert the result of this function into a DB table using shp2pgsql tool


    #method to generate URLs based on user input data, then grab isochrones from the address and insert into database
    def generateIsochrones(self):

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
        count = 0
        failCount = 0
        successCount = 0
        escapeFlag = False


        #TODO look into optimizing string concatenation for generating the URLs: it's inefficient in Java, is Python the same?

        #outer loop: for each point in gridpoints
        def proc(point):
            #get x and y coords from each gridpoint
            #NOTE: in URL, order is (y,x) rather than (x,y), per Ben's example URL
            #truncate to 8 decimal places
            x = '%.5f'%(point[0])
            y = '%.5f'%(point[1])

            #reset cursor to the beginning of the desired time increment
            timeCursor = self.startTime
            
            #inner loop: for each 5 minute increment in time period:
            while timeCursor <= self.endTime:
                url = "http://localhost:8080/otp/routers/default/isochrone?&fromPlace=" + str(y) +"," + str(x) +"&date=" + str(self.startDate) + "&time="+ str(timeCursor.time()) + "&mode=WALK,TRANSIT&cutoffSec=" + str(self.maxTravelTime)
                print(str(count) + "-----" + url)
                count += 1
                
                #request data from URL

                try:
                    response = urllib2.urlopen(url)
                    
                except urllib2.HTTPError as err:
                    #failCount += 1
                    #print("Failed: "+ str(failCount) + url)
                    timeCursor += timedelta(minutes = timeIncrement)
                    continue
                except:
                    #failCount += 1
                    #print("Failed: "+ str(failCount) + url)
                    timeCursor += timedelta(minutes = timeIncrement)
                    continue


                #parse the response as json
                isochrone = json.load(response)

                #write json to a tempfile, hopefully we can eliminate this step
                with open(tempDirectory + "tempiso.json", "w") as f:
                    json.dump(isochrone, f)
                    
                #insert temp json file into db
                #decide whether to append or not: add "-append", to the subprocess command if so
                subprocess.Popen(["ogr2ogr", "-f", "PostgreSQL", "PG:dbname="+ self.dbname + " user=" + self.dbuser + " password=" +self.dbpassword, "-nln","testiso", "-append", tempDirectory+ "tempiso.json"])

                #increment cursor by time increment (5 mins)
                timeCursor += timedelta(minutes = timeIncrement)

                #TODO load isochrone into appropriate database table
                
        p = pools.ThreadPool()
        # print p.map(lambda i: i, range(10))
        test = [1, 2, 3, 4]
        p.amap(lambda point: self.proc(point), gridpoints)
        # print "after Proc"
        p.close()
        p.join()


    #Method to launch help page
    def helpMe(self):
        print("open help file")

    def testFun(self, i):
        print i


#End of Class
#############################################################################################
        
#launch main window
root = Tk()
gui = TransitMappingToolGUI(root)
root.mainloop()
