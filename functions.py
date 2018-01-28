#!/usr/bin/env python

from tkinter import *

import subprocess

import sqlite3

import os

import time

from dbus import glib
glib.init_threads()

import dbus
bus = dbus.SessionBus()



def parseGPX(gpxFilePath):
        gpxFile = open(gpxFilePath,"r")
        strLines = gpxFile.readlines()
        gpxFile.close()
        strTurn = []
        if len(strLines) >= 8:
            for i in range(0,len(strLines)-8):
                if strLines[i+7]:
                    if len(strLines[i+7]) > 61:
                        strTurn.append(i)
                        strTurn[i] = strLines[i+7][61:]
                        strTurn[i] = strTurn[i].split("<name>")[1]
                        strTurn[i] = strTurn[i].split("</name>")[0]
        return strTurn

def do_search(strAddress, gpxFilePath):
    
        stNum = ""
        stName = ""
        ciName = ""
        destLon = ""
        destLat = ""
    
        if strAddress.find(",") > -1:
            addString = strAddress.split(",")
            if not addString[0].find(" ") == -1:
                stString = addString[0].split(" ")
                stNum = str(stString[0])
                stName = str(stString[1:])
                ciName = str(addString[1])
                stName = stName.replace("[","")
                stName = stName.replace("]","")
                stName = stName.replace("'","")
                stName = stName.replace(",","")
                if ciName.find(" ") == 0:
                    ciName = ciName.replace(" ","", 1)
                stName = "%" + stName + "%"
                ciName = "%" + ciName + "%"
                sqlCommand = ('''SELECT DISTINCT lon, lat, number, street, city, district, region FROM addn WHERE number = "{0}" and street LIKE "{1}" and city LIKE "{2}"''').format(stNum, stName, ciName)
        else:
            stString = strAddress.split(" ")
            stNum = str(stString[0])
            stName = str(stString[1:])
            stName = stName.replace("[","")
            stName = stName.replace("]","")
            stName = stName.replace("'","")
            stName = stName.replace(",","")
            stName = "%" + stName + "%"
            sqlCommand = ('''SELECT DISTINCT lon, lat, number, street, city, district, region FROM addn WHERE number = "{0}" and street LIKE "{1}"''').format(stNum, stName)

        db = sqlite3.connect(':memory:')
        db = sqlite3.connect('/home/pi/addresses.db')

        db.row_factory = sqlite3.Row
        
        cursor = db.cursor()

        cursor.execute(sqlCommand)

        for row in cursor:
            destLon = row['lon']
            destLat = row['lat']   
        db.close()
    
        if destLon and destLat:
            
            remote_object = bus.get_object("org.navit_project.navit", "/org/navit_project/navit/default_navit" )

            iface = dbus.Interface(remote_object, dbus_interface="org.navit_project.navit")
    
            iter = iface.attr_iter()
    
            path = remote_object.get_attr_wi("navit",iter)
    
            navit = bus.get_object('org.navit_project.navit', path[1])
    
            iface.attr_iter_destroy(iter)
         
            navit.set_destination("geo: " + destLon + " " + destLat + '"', "Destination")
                        
            navit = dbus.Interface(remote_object, dbus_interface="org.navit_project.navit.navit")
            
            navit.export_as_gpx(gpxFilePath,)
            
            
            
def do_export(gpxFilePath):

    remote_object = bus.get_object("org.navit_project.navit", "/org/navit_project/navit/default_navit" )

    iface = dbus.Interface(remote_object, dbus_interface="org.navit_project.navit")
    
    iter = iface.attr_iter()
    
    path = remote_object.get_attr_wi("navit",iter)
    
    navit = bus.get_object('org.navit_project.navit', path[1])
    
    iface.attr_iter_destroy(iter)
                             
    navit = dbus.Interface(remote_object, dbus_interface="org.navit_project.navit.navit")
            
    navit.export_as_gpx(gpxFilePath,)