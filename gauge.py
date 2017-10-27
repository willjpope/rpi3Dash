import math
import pygame

def gaugeLegend(
                    legendValue,
                    displayValue,
                    positionX,
                    positionY,
                    length,
                    destination,
                    fontSize,
                    doubleLength,
                    drawLine,
                    doubleLine,
                    singleLine,
                    displayDivision,
                    backgroundColour,
                    gaugeDivCol,
                    gaugeDivFontCol
    ):
        position = (positionX,positionY)

        lineLength = doubleLine

        x = position[0] - math.cos(math.radians(legendValue)) * length
        y = position[1] - math.sin(math.radians(legendValue)) * length
        xa = position[0] - math.cos(math.radians(legendValue)) * (length - int(length / lineLength))
        ya = position[1] - math.sin(math.radians(legendValue)) * (length - int(length / lineLength))
        xlabel = position[0] - math.cos(math.radians(legendValue)) * (length - int(length / singleLine))
        ylabel = position[1] - math.sin(math.radians(legendValue)) * (length - int(length / singleLine))
        
        pygame.draw.line(destination, gaugeDivCol, (x,y),(xa,ya), 10)
                

        label = fontSize.render(str(int(displayValue / displayDivision)), 1, gaugeDivFontCol)

        labelRect = label.get_rect()
        labelRect.centerx = int(xlabel)
        labelRect.centery = int(ylabel)
        destination.blit(label, (labelRect))

def gaugeNeedle(
                    needleDestination,
                    needleValue,
                    needleLength,
                    positionX,
                    positionY,
                    fontSize,
                    startPosition,
                    endPosition,
                    gaugeMax,
                    gaugeDivisions,
                    gaugeNeedleCol,
                    gaugeArcCol,
                    gaugeDivCol,
                    gaugeDivFontCol,
                    doubleLine,
                    singleLine,
                    displayDivision,
                    bottomArc,
                    topArc,
                    needleArc,
                    displayNeedle,
                    needLegend,
                    needDivisionLegend
    ):

    position = (positionX,positionY)
    length = needleLength
    length2 = int(needleLength / 20)
    length3 = length2 + 5
    destination = needleDestination
    if needDivisionLegend:
        fontSize = fontSize
    else:
        fontSize = pygame.font.SysFont("DejaVu Math TeX Gyre", 0)
    singleLine = singleLine
    doubleLine = doubleLine
    backgroundColour = (0,0,0)


    degreesDifference = 360 - (startPosition + (180 - endPosition))
    value = int((needleValue * (degreesDifference / (gaugeDivisions * (gaugeMax/10)))) + startPosition)
    displayValue = (needleValue * (degreesDifference / (gaugeDivisions* (gaugeMax/10)))) + startPosition

    x = position[0] - math.cos(math.radians(value)) * (length - int(length / singleLine))
    y = position[1] - math.sin(math.radians(value)) * (length - int(length / singleLine))
    x2 = position[0] - math.cos(math.radians(value - 90)) * length2
    y2 = position[1] - math.sin(math.radians(value - 90)) * length2
    x3 = position[0] - math.cos(math.radians(value + 180)) * length3
    y3 = position[1] - math.sin(math.radians(value + 180)) * length3
    x4 = position[0] - math.cos(math.radians(value + 90)) * length2
    y4 = position[1] - math.sin(math.radians(value + 90)) * length2

    xa = position[0] - math.cos(math.radians(value)) * length
    ya = position[1] - math.sin(math.radians(value)) * length
    xa2 = x - math.cos(math.radians(value))
    ya2 = y - math.sin(math.radians(value))
    xa3 = x - math.cos(math.radians(value + 180))
    ya3 = y - math.sin(math.radians(value + 180))
    xa4 = x - math.cos(math.radians(value + 90)) * (length2 + 4)
    ya4 = y - math.sin(math.radians(value + 90)) * (length2 + 4)

    valueDivisions = degreesDifference/(gaugeMax/gaugeDivisions)

    gaugeLegend(startPosition, 0, position[0], position[1], length,
                        destination, fontSize,False,True,doubleLine,singleLine,1,backgroundColour, gaugeDivCol, gaugeDivFontCol)

    for divisions in range(1,(gaugeMax//gaugeDivisions)):
        
        if needleValue >= (gaugeDivisions * divisions):
            gaugeLegend((startPosition + (valueDivisions * divisions)), (gaugeDivisions * divisions),
                                position[0], position[1], length, destination, fontSize, True, True, doubleLine,
                                singleLine, 1, backgroundColour, gaugeDivCol, gaugeDivFontCol)

    #if displayNeedle:
    #pygame.draw.aalines(destination, RED, True, ((x,y), (x2,y2), (x3, y3), (x4, y4)), False) #who knows

    if bottomArc:
        pygame.gfxdraw.arc(destination,position[0],position[1],
                       (length - int(length / singleLine)),(180 + value),endPosition,  gaugeArcCol) #BOTTOM ARC
    
    if displayNeedle:
        pygame.draw.aaline(destination, gaugeNeedleCol, (x,y),(xa,ya), False) #NEEDLE

    if topArc:
        pygame.gfxdraw.arc(destination,position[0],position[1],
                       length,(180 + startPosition), (value - 180), gaugeArcCol) #TOP ARC

    if needleArc:
        pygame.gfxdraw.arc(destination,position[0],position[1],
                       (length - int(length / doubleLine)),(180 + startPosition) , (value - 180), gaugeArcCol) #NEEDLE ARC

    if needLegend:
        gaugeLegend((180 + endPosition), needleValue , position[0], position[1],
                        length, destination, fontSize, False, False,
                        doubleLine,singleLine,1,backgroundColour, gaugeDivCol, gaugeDivFontCol)