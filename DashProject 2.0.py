import sys
import logging
import os
import pygame
import time
import math
from pygame.locals import *
from PyQt4 import QtGui
from PyQt4 import QtCore

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

class ImageWidget(QtGui.QWidget):
    def __init__(self,surface,parent=None):
        super(ImageWidget,self).__init__(parent)
        w=surface.get_width()
        h=surface.get_height()
        self.data=surface.get_buffer().raw
        self.image=QtGui.QImage(self.data,w,h,QtGui.QImage.Format_RGB32)

    def paintEvent(self,event):
        qp=QtGui.QPainter()
        qp.begin(self)
        qp.drawImage(0,0,self.image)
        qp.end()


class MainWindow(QtGui.QMainWindow):
    def __init__(self,surface,parent=None):
        super(MainWindow,self).__init__(parent)
        self.setCentralWidget(ImageWidget(surface))

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

#screen = pygame.display.set_mode(size)

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

s=pygame.Surface((1024,800))
app = QtGui.QApplication( sys.argv )
w = MainWindow(s)
w.show()
container = QtGui.QX11EmbedContainer( w )
container.show()
winId = container.winId()
process = QtCore.QProcess(container)
os.environ['MODRANA_XID'] = str( winId )
process.startDetached("modrana")
app.exec_()

if testing == False:
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

speedoMax = 160
speedoDivisions = 10
speedoFont = pygame.font.SysFont("Droid Sans", 30)

rpmMax = 7000
rpmDivisions = 500
rpmFont = pygame.font.SysFont("DejaVu Math TeX Gyre", 0)

KPH_Value = 0
RPM_Value = 0
    



while True:

    for event in pygame.event.get():

        if event.type==pygame.QUIT:
            sys.exit()

        if event.type is KEYDOWN and event.key == K_q:
            sys.exit()
            
    surface1.fill(0x000000)
    surface2.fill(0x0000FF)
    surface3.fill(0x0000FF)
    surface4.fill(0x0000FF)
    surface5.fill(0x0000FF)
    surface6.fill(0x0000FF)
    
    if testing == True:
        if KPH_Value >=115:
            speedoNeedleCol = RED
            speedoArcCol = RED
            speedoDivCol = RED
            speedoFontCol = RED
        elif KPH_Value >= 100:
            speedoNeedleCol = GREEN
            speedoArcCol = GREEN
            speedoDivCol = GREEN
            speedoFontCol = GREEN
        elif KPH_Value >= 80:
            speedoNeedleCol = PURPLE
            speedoArcCol = PURPLE
            speedoDivCol = PURPLE
            speedoFontCol = PURPLE
        elif KPH_Value >= 50:
            speedoNeedleCol = BLUE
            speedoArcCol = BLUE
            speedoDivCol = BLUE
            speedoFontCol = BLUE  
        else:
            speedoNeedleCol = WHITE
            speedoArcCol = WHITE
            speedoDivCol = WHITE
            speedoFontCol = WHITE

        if RPM_Value >= 4500:
            rpmNeedleCol = RED
            rpmArcCol = RED
            rpmDivCol = RED
            rpmFontCol = RED
        elif RPM_Value >= 800:
            rpmNeedleCol = BLUE
            rpmArcCol = BLUE
            rpmDivCol = BLUE
            rpmFontCol = BLUE  
        else:
            rpmNeedleCol = WHITE
            rpmArcCol = WHITE
            rpmDivCol = WHITE
            rpmFontCol = WHITE


    if testing == False:
        text = str(port.sensor('rpm'))
        text = text.split(",")[1].strip()
        text = int(float(text))
        print(text)
        gauge.gaugeNeedle(surface1, KPH_Value, 648, 650, 650, speedoFont, 45, -45, speedoMax, speedoDivisions, speedoNeedleCol, speedoArcCol, speedoDivCol, speedoFontCol, 12, 6, 1, False, False, False, False, True, True)
    else:
        gauge.gaugeNeedle(surface1, KPH_Value, 648, 650, 650, speedoFont, 45, -45, speedoMax, speedoDivisions, speedoNeedleCol, speedoArcCol, speedoDivCol, speedoFontCol, 12, 6, 1, False, False, False, False, False, True)
        gauge.gaugeNeedle(surface1, RPM_Value, 148, 150, 150, rpmFont, -80, -10, rpmMax, rpmDivisions, rpmNeedleCol, rpmArcCol, rpmDivCol, rpmFontCol, 6, 3, 1, False, False, False, False, False, False)
        #gauge.gaugeBar(surface1, KPH_Value, 150, 100, 100, speedoFont, 45, -45, speedoMax, speedoDivisions, speedoNeedleCol, speedoArcCol, speedoDivCol, speedoFontCol, 12, 6, 1, False, False, False, False, False, True)
    
    screen.blit(surface1,(surface1X,surface1Y))
    screen.blit(surface2,(surface2X,surface2Y))
    screen.blit(surface3,(surface3X,surface3Y))
    screen.blit(surface4,(surface4X,surface4Y))
    screen.blit(surface5,(surface5X,surface5Y))
    screen.blit(surface6,(surface6X,surface6Y))

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
                        
