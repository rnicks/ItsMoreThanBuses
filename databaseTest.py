#!/usr/bin/python



import psycopg2
import subprocess

tables = (
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




connString = "host='localhost' dbname='transitDatabase'  user='robertnickerson' password='velcro'"


dbConnection = psycopg2.connect(connString)
dbCursor =  dbConnection.cursor()





dbCursor.execute(""" CREATE TABLE GridPoints(
        g_id INTEGER PRIMARY KEY,

        geom FLOAT(8),

        x FLOAT(8),

        y FLOAT(8),

        loc_id INTEGER)""")





