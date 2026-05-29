from time import sleep
import argparse
import pyautogui
import PIL
import os

parser = argparse.ArgumentParser(
    prog='ImageClicker',
    description='finds an image on screen and clicks it one or more times'
)

parser.add_argument('filenames', nargs='+')
parser.add_argument('-c', '--count', type=int, default=1, help="times to click, values less than 0 for infinite clicks")
parser.add_argument('-v', '--verbose', default=False, action='store_true')
parser.add_argument('-s', '--sleep', type=float, default=0.01, help="time to sleep after each click OR each failed search")
parser.add_argument('-t', '--threshold', type=float, default=0.9, help="image matching confidence")
parser.add_argument('-z', '--zero', default=False, action='store_true', help="move cursor to 0,0 after each click")
parser.add_argument('-g', '--grayscale', default=False, action='store_true', help='search in grayscale for 30%% performance boost')

args = parser.parse_args()

if args.count <= 0: args.count = float('inf')

pyautogui.PAUSE = args.sleep  # Default is 0.1



def printDebug(string):
    if args.verbose: print(string)

printDebug(args)


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
        
        
        clickSuccess = False
        for imageData in imageDataList:
            
            pos = None
            try:
                pos = pyautogui.locateCenterOnScreen(imageData)
                printDebug("Found "+str(pos))
            except: pass
            
            if pos:
                try:
                    printDebug("clicking "+str(pos))
                    pyautogui.click(pos)
                    
                    clickSuccess = True
                    
                    if args.zero: pyautogui.moveTo(1,1)
                except Exception as e: printDebug(e)
        
        if clickSuccess:
            clicksDone = clicksDone + 1
            printDebug('clicked: ' + str(clicksDone) + '/' + str(args.count))
            
        


main(args)
