#!/usr/bin/env python3

import sys
import logging
import os
import pygame
import time
import math
from pygame.locals import *
from tkinter import *
import inputbox
import functions

import gauge

from obdython import Device, OBDPort 

#import serial
#import string
#import time
#import platform
#import inspect
#import socket
#import bluetooth
#from math import ceil
#import logging

testing = True

if testing == False:
    dev = Device(Device.types['bluetooth'], bluetooth_mac="00:1D:A5:68:98:8D", bluetooth_channel=1)
    port = OBDPort(dev)
    time.sleep(0.1)
    port.connect()  
    time.sleep(0.1)
    port.ready()  


os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'

pygame.init()

size = width, height = 1320, 740

monitorX = pygame.display.Info().current_w
monitorY = pygame.display.Info().current_h

surface1X = (monitorX / 2) - 650
surface1Y = (monitorY / 2) - 360

surface2X = (monitorX / 2) - 500
surface2Y = (monitorY / 2) - 210

surface3X = (monitorX / 2) - 650
surface3Y = (monitorY / 2) - 360

surface4X = (monitorX / 2) + 310
surface4Y = (monitorY / 2) - 360

surface5X = (monitorX / 2) - 310
surface5Y = (monitorY / 2) + 60

surface6X = (monitorX / 2) + 10
surface6Y = (monitorY / 2) + 60

screen = pygame.display.set_mode(size)

surface1 = pygame.Surface((1300,720))
surface2 = pygame.Surface((1000,600))
surface3 = pygame.Surface((340,340))
surface4 = pygame.Surface((340,340))
surface5 = pygame.Surface((300,300))
surface6 = pygame.Surface((300,300))

surface2.set_colorkey(0x0000FF)
surface3.set_colorkey(0x0000FF)
surface4.set_colorkey(0x0000FF)
surface5.set_colorkey(0x0000FF)
surface6.set_colorkey(0x0000FF)

if testing == True:
    pygame.display.set_mode((monitorX,monitorY), FULLSCREEN)

screen.fill(0x000000)

pygame.mouse.set_visible(False)

fifteen = pygame.font.SysFont("Droid Sans", 15)

twenty = pygame.font.SysFont("Droid Sans", 18)

sixty = pygame.font.SysFont("DejaVu Math TeX Gyre", 60)

BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0, 255, 0)
PINK = (255,105,180)
PURPLE = (128,0,128)
WHITE = (255,255,255)
BLUE = (0,0,255)
highlighterGreen = (57,255,20)

speedoMax = 160
speedoDivisions = 10
speedoFont = pygame.font.SysFont("Droid Sans", 30)

rpmMax = 7000
rpmDivisions = 500
rpmFont = pygame.font.SysFont("DejaVu Math TeX Gyre", 0)

KPH_Value = 0
RPM_Value = 0
    
fixedSpeedCol = highlighterGreen
fixedRPMCol = highlighterGreen

oldSearch = ""
gpxFilePath = "/home/pi/Desktop/DashProject/route.gpx"
textinput = inputbox.TextInput("pygame-font",50,True, WHITE)
tbtsurface = sixty.render("", False, (255, 255, 255))

while True:
    
    
 
    events = pygame.event.get()
    for event in events:

        if event.type==pygame.QUIT:
            sys.exit()
        if testing == True:
            if event.type is KEYDOWN and event.key == K_q:
                sys.exit()
            if event.type is KEYDOWN and event.key == K_RETURN:
                print("searching")
                if not oldSearch == textinput.get_text() or oldSearch == Left(textinput.get_text(), Len(textinput.get_text())-1):
                    functions.do_search(textinput.get_text(), gpxFilePath)
                    oldSearch = textinput.get_text()
           
            
    print("exporting")
    functions.do_export(gpxFilePath)
    surface1.fill(0x000000)
    surface2.fill(0x0000FF)
    surface3.fill(0x0000FF)
    surface4.fill(0x0000FF)
    surface5.fill(0x0000FF)
    surface6.fill(0x0000FF)
    
    textinput.update(events)
    # Blit its surface onto the screen
    surface2.blit(textinput.get_surface(), (150, 350))
    
    
    if testing == True:
        if KPH_Value >=101:
            speedoNeedleCol = RED
            speedoArcCol = RED
            speedoDivCol = RED
            speedoFontCol = RED
        #elif KPH_Value >= 100:
        #    speedoNeedleCol = GREEN
        #    speedoArcCol = GREEN
        #    speedoDivCol = GREEN
        #    speedoFontCol = GREEN
        #elif KPH_Value >= 80:
        #    speedoNeedleCol = PURPLE
        #    speedoArcCol = PURPLE
        #    speedoDivCol = PURPLE
        #    speedoFontCol = PURPLE
        #elif KPH_Value >= 50:
        #    speedoNeedleCol = BLUE
        #    speedoArcCol = BLUE
        #    speedoDivCol = BLUE
        #    speedoFontCol = BLUE  
        else:
            speedoNeedleCol = highlighterGreen
            speedoArcCol = highlighterGreen
            speedoDivCol = highlighterGreen
            speedoFontCol = highlighterGreen

        if RPM_Value >= 3500:
            rpmNeedleCol = RED
            rpmArcCol = RED
            rpmDivCol = RED
            rpmFontCol = RED  
        else:
            rpmNeedleCol = (2,103,255)
            rpmArcCol = (2,103,255)
            rpmDivCol = (2,103,255)
            rpmFontCol = (2,103,255)


    if testing == False:
        text = str(port.sensor('rpm'))
        text = text.split(",")[1].strip()
        text = int(float(text))
        print(text)
        text = str(port.sensor('rpm'))
        text = text.split(",")[1].strip()
        text = int(float(text))
        print(text)
        text = str(port.sensor('rpm'))
        text = text.split(",")[1].strip()
        text = int(float(text))
        print(text)

        gauge.gaugeNeedle(surface1, KPH_Value, 648, 650, 650, speedoFont, 45, -45, speedoMax, speedoDivisions, speedoNeedleCol, speedoArcCol, speedoDivCol, speedoFontCol, 12, 6, 1, False, False, False, False, True, True)
    else:
        #gauge.gaugeBar(surface1, KPH_Value, 248, 0, 545, speedoFont, 45, -45, speedoMax, speedoDivisions, speedoNeedleCol, speedoArcCol, speedoDivCol, speedoFontCol, 12, 6, 1, False, False, False, False, False, False)
        gauge.gaugeNeedle(surface1, speedoMax, 248, 300, 300, speedoFont, -80, 50, speedoMax, speedoDivisions, fixedRPMCol, fixedRPMCol, fixedRPMCol, fixedRPMCol, 9, 6, 1, False, False, False, False, False, True)
        gauge.gaugeNeedle(surface1, rpmMax, 148, 300, 300, rpmFont, -80, 50, rpmMax, rpmDivisions, fixedSpeedCol, fixedSpeedCol, fixedSpeedCol, fixedSpeedCol, 6, 3, 1, False, False, False, False, False, False)
        gauge.gaugeNeedle(surface1, RPM_Value, 148, 300, 300, rpmFont, -80, 50, rpmMax, rpmDivisions, rpmNeedleCol, rpmArcCol, rpmDivCol, rpmFontCol, 6, 3, 1, False, False, False, False, False, False)
        gauge.gaugeNeedle(surface1, KPH_Value, 248, 300, 300, speedoFont, -80, 50, speedoMax, speedoDivisions, speedoNeedleCol, speedoArcCol, speedoDivCol, speedoFontCol, 9, 6, 1, False, True, True, True, True, True)
        #gauge.gaugeBar(surface1, KPH_Value, 248, 0, 545, speedoFont, 45, -45, speedoMax, speedoDivisions, speedoNeedleCol, speedoArcCol, speedoDivCol, speedoFontCol, 12, 6, 1, False, False, False, False, False, False)
        if functions.parseGPX(gpxFilePath):
            tbtsurface.fill(0x0000FF)
            screen.blit(tbtsurface,(0,0))
            tbtsurface = sixty.render(functions.parseGPX(gpxFilePath)[0], False, (255, 255, 255))
        else:
            tbtsurface = sixty.render("NO DATA", False, (255, 255, 255))
    
    
    screen.blit(surface1,(surface1X,surface1Y))
    screen.blit(surface2,(surface2X,surface2Y))
    screen.blit(surface3,(surface3X,surface3Y))
    screen.blit(surface4,(surface4X,surface4Y))
    screen.blit(surface5,(surface5X,surface5Y))
    screen.blit(surface6,(surface6X,surface6Y))
    screen.blit(tbtsurface,(0,0))



    time.sleep(0.1)

    if KPH_Value < speedoMax:
        KPH_Value = KPH_Value + 1
    else:
        KPH_Value = 30
        
    if RPM_Value < rpmMax:
        RPM_Value = RPM_Value + 100
    else:
        RPM_Value = 700

    pygame.display.update()
                        