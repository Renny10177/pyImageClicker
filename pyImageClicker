from time import sleep
import argparse
import pyautogui
import math
import PIL
import os

parser = argparse.ArgumentParser(
    prog='ImageClicker',
    description='finds an image on screen and clicks it one or more times'
)

parser.add_argument('filenames', nargs='+')
parser.add_argument('-c', '--count', type=int, default=1) # values less than 0 for infinite clicks
parser.add_argument('-v', '--verbose', default=False, action='store_true')
parser.add_argument('-s', '--sleep', type=float, default=0.2)
parser.add_argument('-t', '--threshold', type=float, default=0.9)

args = parser.parse_args()

if args.count <= 0: args.count = math.infinity




def printDebug(string):
    if args.verbose: print(string)

printDebug(args)

def findImagesOnScreen(imageDataList): #takes a list of Image objects and searches for each one, returning a list of Position objects
    output = []
    for imageData in imageDataList:
        try:
            output.append(pyautogui.locateCenterOnScreen(imageData))
        except Exception as e:
            printDebug(e)
    return output


def loadImages(filenames): #takes list of filenames and outputs list of ImageWrapper objects
    imageDataList = []
    for filename in filenames:
        printDebug('loading image ' + str(os.path.realpath(filename)))
        imageDataList.append(PIL.Image.open(os.path.realpath(filename)))
    return imageDataList


def main(args):
    
    imageDataList = loadImages(args.filenames)
    
    
    clicksDone = 0
    while clicksDone < args.count:
        
        positionsFound = findImagesOnScreen(imageDataList)
        printDebug("positions found: " + str(positionsFound))
        
        if not positionsFound:
            continue
            
        for position in positionsFound:
            printDebug("Clicking at " + str(position))
            pyautogui.click(position[0], position[1])
            clicksDone = clicksDone + 1
            
        sleep(args.sleep)


main(args)
