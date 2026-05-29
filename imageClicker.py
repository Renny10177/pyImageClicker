import argparse
import pyautogui
import cv2
import PIL
import os
import numpy as np 

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
#parser.add_argument('-g', '--grayscale', default=False, action='store_true', help='search in grayscale for 30%% performance boost')

args = parser.parse_args()

if args.count <= 0: args.count = float('inf')

pyautogui.PAUSE = args.sleep  # Default is 0.1



def printDebug(string):
    if args.verbose: print(string)

printDebug(args)


def loadImages(filenames):
    imageDataList = []

    for filename in filenames:
        printDebug('loading image ' + str(os.path.realpath(filename)))

        template = cv2.imread(os.path.realpath(filename), cv2.IMREAD_COLOR)

        hh, ww = template.shape[:2]

        mydict = {
            "template": template,
            "hh": hh,
            "ww": ww
        }

        imageDataList.append(mydict)

    return imageDataList


def getScreenshot():
    return cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
def locateCenterOnScreen(imageData):
    screen = getScreenshot()

    correlation = cv2.matchTemplate(
        screen,
        imageData["template"],
        cv2.TM_CCOEFF_NORMED
    )

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(correlation)

    printDebug(f"max correlation: {max_val}")

    if max_val >= args.threshold:
        x = max_loc[0] + imageData["ww"] // 2
        y = max_loc[1] + imageData["hh"] // 2
        return (x, y)

    return None


def main(args):
    
    imageDataList = loadImages(args.filenames)
    clicksDone = 0
    
    while clicksDone < args.count:
        
        clickSuccess = False
        
        for imageData in imageDataList:
            
            pos = None
            
            try:
                pos = locateCenterOnScreen(imageData)
                printDebug("Found "+str(pos))
                
            except Exception as e:
                printDebug(e)
            
            if pos:
                try:
                    printDebug("clicking "+str(pos))
                    
                    pyautogui.click(x=pos[0], y=pos[1])
                    
                    clickSuccess = True
                    
                    if args.zero:
                        pyautogui.moveTo(1,1)
                        
                        
                except Exception as e:
                    printDebug(e)
        
        if clickSuccess:
            clicksDone = clicksDone + 1
            
            printDebug('clicked: ' + str(clicksDone) + '/' + str(args.count))
            
        


main(args)
