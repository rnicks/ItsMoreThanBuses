
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

connString = "host='localhost' dbname='test' user='robertnickerson' password='velcro'"


def generateGrid():


    #try connecting to the database
    try:
        conn = psycopg2.connect(connString)
    except:
        print("Database connection error")

    dbCursor = conn.cursor()

    dbCursor.execute("""DROP TABLE IF EXISTS boundingbox;""")
    
    conn.commit()

    dbCursor.execute("""
        
    SELECT * into boundingbox FROM
        (SELECT ST_SetSRID(ST_Extent(way),4326) as box FROM (
         SELECT way FROM planet_osm_polygon
         UNION
         SELECT way FROM planet_osm_point
         UNION
         SELECT way FROM planet_osm_line
         UNION
         SELECT way FROM planet_osm_roads) as extents) as bextent
    ;""")
    
    conn.commit()

def getMinMax():


    #try connecting to the database
    try:
        conn = psycopg2.connect(connString)
    except:
        print("Database connection error")

    dbCursor = conn.cursor()

    dbCursor.execute("""select st_xmin(box) from boundingbox""")
    xmin = dbCursor.fetchall()[0]
    print (xmin)

    dbCursor.execute("""select st_xmax(box) from boundingbox""")
    xmax = dbCursor.fetchall()[0]
    print (xmax)

    dbCursor.execute("""select st_ymin(box) from boundingbox""")
    ymin = dbCursor.fetchall()[0]
    print (ymin)

    ymax = dbCursor.execute("""select st_ymax(box) from boundingbox""")
    ymax = dbCursor.fetchall()[0]
    print (ymax)
    


generateGrid()
getMinMax()
