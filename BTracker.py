import sys
import cv2
from random import randint
import platform
import datetime
import os
import threading
import random
import psutil  # for keeping track of OS
import time  # keeping track of system time
from imutils.video import FPS
from datetime import datetime

# class for the tracker


class tracker(object):
    def __init__(self, trackID):
        self.trackID = trackID

# writing system requirements


def File():
    # Testing each method
    print("File Method has started")
    now = datetime.now()
    dtStr = now.strftime("%d.%m.%Y_%H.%M")
    filename = dtStr+".txt"
    file = open(filename, "w")
    file.write("Machine (Bit): " + platform.machine() + "\n")
    file.write("Machine - Version: " + platform.version() + " \n")
    file.write("Machine - Platform: " + platform.platform() + "\n")
    file.write("Machine - System: " + platform.system() + "\n")

    psutil.virtual_memory()
    file.write("Virtual Memory - Avaliable : " +
               str(psutil.virtual_memory().percent) + "\n")


# Writing the system processes
# def running():

# The file being rested
# def processedTxt():

# loop for the trackers
# def loopingTracker():


def main():
    # starting timer
    start = time.time()

    # File()
    print("File method has ended")
    # Set video to load
    videoPath = "TownCentreXVID.avi"

    cap = cv2.VideoCapture(videoPath)
    if cv2.waitKey(1) & 0xFF == 27:
		break


# Destorying all windows
cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
