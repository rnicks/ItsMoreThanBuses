It’s More Than Buses
OSX Installation Instructions


 Install Homebrew: https://brew.sh/
a.  Per Homebrew instructions, type: /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" in Terminal
b.  Update homebrew: type “brew update” then “brew doctor” from Terminal
 Install PostgreSQL
a.  Type “brew install postgresql” from Terminal
 Install PostGIS extension for PostgreSQL:
a.  Type “brew install postgis” from Terminal
 Create a database
a.  Type “createdb ‘your_database_name’ from Terminal
 Install Python 2.7:
a.  Type “brew install python” from Terminal
 Install GDAL/ogr2ogr:
a.  Type “brew install gdal” from Terminal
 Install psycopg2
a.  Type “pip install psycopg2” from Terminal (note: pip is a Python tool, and requires a Python installation to function)
 Install OpenTripPlanner:
a.  Go to: https://repo1.maven.org/maven2/org/opentripplanner/otp/
b.  navigate to the directory for the highest version number, and download the file whose name ends with “.shaded.jar” e.g. “otp-1.2.0-shaded.jar”
 Get an OpenStreetMaps (OSM) extract for your desired service area
a.  https://export.hotosm.org/en/v3/ can be used to create a custom extract
Get a General Transit Feed Specification (GTFS) file for your transit service
a.  Ex: Halifax Metro Transit data can be found here https://www.halifax.ca/home/open-data/halifax-transit-open-data

Create a custom point grid for your desired area using QGIS
a.  See separate instructions for this step
Create a folder to store both the OSM and GTFS files. These MUST be located in the same folder.
Launch the tool
a.  Open Terminal, navigate to the folder containing the tool, type “python nameoftool.py”


It’s More Than Buses 
Windows Installation Instructions 


Install PostgreSQL 
a. Run .exe file 
Install PostGIS extension for PostgreSQL: 
a. Run “Application stack builder” tool, that was installed with postgreSQL 
Create a database 
a. Type “createdb ‘ your_database_name’ from command line 
b. Make sure to open pgAdmin to check that users have correct permissions and passwords are setup to be the expected values. 
I nstall Python 2.7 from Miniconda : https://conda.io/miniconda.html 
a. Run .exe file 
Install G DAL/ogr2ogr: https://anaconda.org/conda - forge/gdal 
a. Type “ conda install -c conda -forge gdal” in command line 
Install psycopg2 
a. Type “pip install psycopg2” in command line (note: pip is a Python tool, and requires a Python installation to function) 
Install O penTripPlanner: 
a. Go to: https://repo1.maven.org/maven2/org/opentripplanner/otp/ 
b. navigate to the directory for the highest version number, and download the file whose name ends with “ .shaded.jar ” e.g. “otp - 1.2.0 - shaded.jar” 
Get an OpenStreetMaps (OSM) extract for your desired service area 
a. https://export.hotosm.org/en/v3/ can be used to create a custom extract 
Get a General Transit Feed S pecification (GTFS) file for your transit service 
a. Ex: Halifax Metro Transit data can be found here https://www.halifax.ca/home/open-data/halifax-transit-open-data 
Create a custom point grid for your desired area using QGIS 
a. See separate instructions for this step 
Create a folder to store both the OSM and GTFS files. These MUST be located in the same folder. 
Launch the tool 
a. Open command line, navigate to the folder containing the tool, type “python TransitMappingTool.py” 


Performance Optimization 

Our client approached us for this project for two purposes. First, to automate the process of their software. Second, to improve the performance of the ir software. Our group approached performance optimization on this project from the application, and the database perspective . 

Application 
From the application perspective , our group improved the performance for the software in two ways. First, we took the process which generated the isochrones and improved it by skipp ing the s tep which converted the isochrones to shapefile and instead converted the isoch r ones from G eo JSON directed to the P ost GIS format that we needed for the analysis . Second, we automated this process of generating isochrones, and thereby significantly improved the usability of the software. 

Database 
Our team used the client’s original database for the first half of the project. Once we determined that the clients original database was a source of major performance problems, our team decided to create a new dat abase with a new design and structure. After consulting with the client, we built the database. 
From the PSQL query perspective , we conducted four approaches into database performance improvemen t. Three of these studies did not succeed, whilst the fourth gave us great success. 
First, t o reduce the number of database calls, we decided to do the calculation of overlapping isochrones in the application instead of the python code. To do this, we sought to pull the x, y coordinates of the gridpoints, their geom data, and store it into a python list. Then, we would go to our isochrones, and pull their geom data, and put it into another python list. Then, we would conduct a comparison on them to determined if their x,y coordinates overlapped. The problem with this approach was that an isochrone, as opposed to a gridpoint, is not a single point. It instead can be a polygon or line, which roughly corresponds to the route that a bus would take. As a result, doing a simple comparison b etween the x, y coordinates of the gridpoint against the x, y coordinates of the isochrone would not work. Our conclusion was that our hypothesis that the performance would be improved by doing the comparison on the application side vs the database side may still be correct, however it is impossible for us to conduct the comparison. 
Our second study into performance improvement came with using the ST_Intersects command in PostGIS. This command takes two geom’s and compares them to see if their locations overlap and reports a boolean . If this was found to be true, then we would increment a counter on a gridpoint which would indicate how many isochrones overlapped a certain gridpoint. After completing this analysis, we would feed this data into another function which would generate a r aster file. The problem with this approach was that the performance of the database was much worse than with the client’s original command. Although the PSQL query we designed for this operation was much smaller, less intensive, and less taxing on the data base, it still required approximately over a million database calls, as it was checking every isochrone against every 
gridpoint individually. Over approximately 60000 gridpoints and 20000 isochrones, this approach become totally unfeasible. Our team quickl y decided to abandon this approach. 
Third, our group attempted to use a PostGIS command called ST_Collects, which takes a large list of mulitpolygons and unifies them into a single polygons. Our team thought that this would improve the performance greatly as we would be conducting the comparison on the gridpoints and only one or two large unified isochrones instead of the original approximately 12000. Unfortunately, despite three of our members spending approximately 3 - 5 days on this command we were unable to get a unified isochrone. Although our PSQL query was running, there was no indication when we analyzed the results in a database tool called PgAdmin that the results were truly unified. Thousands of rows of data still appeared as opposed to the single r ow we were expecting. This would, as a result, not have improved our process at all, as we would still have thousands of database calls. As a result, we once again decided that this approach was not feasible. 
Our successful approach on this database used the original query that the client was using, modified for our database. Results were excellent. As opposed to the 3 hours that the query took on their original database, which the client shortened to 20 - 30 minutes by opening multiple instances of the prog ram, our query took 2 - 3 minutes. That is a tremendous improvement in performance and our team is very pleased with the result. Although we are not certain why the performance of database had such a major improvement, w e believe that the improvement could b e due to the new database structure and design. 
Although three of our studies did not yield favourable results, and from a software development we can conclude that they were unsuccessful, we consider these studies as very valuable and beneficial from the perspective of research. As Thomas Edison said, “I have not failed. I’ve just found 10000 ways that wont work”. 

Isochrone Generation 

Our team uses a multistep process to generate the isochrone by automating the clients existing process : 
First, our client has provided an example URL that we store. Then, we save user entered variables for all the values, such as target travel time in minutes , date range, start time and end time . Next, we get the x, y coordinates of the grid points which we have previously generated in another function. To generates the URL’s that we will use to generate the isochrones, we combine all these values. Using those URL s we form a connection to OpenTripPlanner. OpenTripPlanner then generates a GeoJSON . The GeoJSON is downloaded and saved into a temporary file on the disk. After the file is saved, we convert it into PostGIS format using a tool called OGR2OGR, that we then insert it into the database. In a set of nested for loops, we then repeat this process for each time increment for each gridpoint by going through each gridpoint (x,y) and cycling through a client defined t ime period of 5 minutes. This generates the isochrones for the entire analysis. 

Launching OpenTripPlanner 
Our team also automated the processes to launch OpenTripPlanner. Orginally, OpenTripPlanner was launched by opening command line, navigating to a fo lder which had a OpenTripPlanner - Master folder which had a .jar file that we would run using CMD through a command. This would then launch O pen T rip P lanner. This process was complex, manual, and tedious. Our team automated this process by linking to a butto n which would open CMD and send the relevant command automatically. 
