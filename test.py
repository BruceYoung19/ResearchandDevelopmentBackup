from __future__ import print_function
import sys
import cv2
from random import randint
import platform
import datetime
import os
import psutil #for keeping track of OS
import time #keeping track of system time
from imutils.video import FPS


kcf_ = cv2.TrackerKCF_create()

# Set video to load
videoPath = "TownCentreXVID.avi"

# Create a video capture object to read videos
cap = cv2.VideoCapture(videoPath)

# Read first frame
success, frame = cap.read()
# quit if unable to read the video file
if not success:
  print('Failed to read video')
  sys.exit(1)

# Writing a file
file = open("ComputerSpecs.txt","w")

# writing system requirements
file.write("Machine (Bit): " + platform.machine() + "\n")
file.write("Machine - Version: " + platform.version() +" \n")
file.write("Machine - Platform: " + platform.platform() + "\n")
file.write("Machine - System: " + platform.system()+ "\n")

psutil.virtual_memory()
file.write("Virtual Memory - Avaliable : "  + str(psutil.virtual_memory().percent) + "\n")

# Create MultiTracker object
multiTracker = cv2.MultiTracker_create()

# Initialize MultiTracker
# for bbox in bboxes:
#   multiTracker.add(kcf_, frame, bbox)
#   print(bbox)
box = [(250, 782, 125, 296),(1449, 35, 92, 163), (879,70,65,164),(1651,123,64,158),(715,238,66,172),(1608,609,111,249),(803,255,54,166),(1800,184,67,168),(871,390,113,182),(983,3,51,123),(1349,19,56,109),(1567,910,153,170),(1159,0,37,76),(282,277,84,198),(907,479,120,157),(608,79,88,109),(1349,65,48,83),(1645,705,67,83),(1535,240,96,84),(608,273,122,140),(1511,92,34,97)]

# create a new object tracker for the bounding box and add it
# to our multi-object tracker
for i in box:
	tracker = cv2.TrackerKCF_create()
	multiTracker.add(tracker, frame, i)

#start timer
start = time.time()

#flag for fps counter
flag = False

# Process video and track objects
while cap.isOpened():
	success, frame = cap.read()
	if not success:
		break
	if success and not flag:
		fps = FPS().start()
		flag = True

	# get updated location of objects in subsequent frames
	trackSuccess, boxes = multiTracker.update(frame)
	# update the FPS counter
	fps.update()
	fps.stop()

	pid = os.getpid()
	py = psutil.Process(pid)
	# memoryUse = str(py.memory_info()[0]/2.**30) # memory use in GB...I think
	rssUse = str(py.memory_info()[0]) #memory in bytes
	vmsUse = str(py.memory_info()[1])
	
	file.write("Boundary Box : " + str(frame)+ "\n")
	file.write("FPS: {:.2f}".format(fps.fps())+" - ");
	file.write ("memory use:"+ rssUse + "\n")

	# draw tracked objects
	for i, newbox in enumerate(boxes):
		p1 = (int(newbox[0]), int(newbox[1]))
		p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
		cv2.rectangle(frame, p1, p2, (0, 255, 0), 2, 1)

	# show frame
	cv2.imshow('MultiTracker', frame)

	# quit on ESC button
	if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
		break


#end timer
end = time.time();
timeSec = end - start;
timeMin = str(timeSec/60);

file.write("time elasped: "+ str(timeSec) +"seconds - "+timeMin+" minutes.");
 # close all windows
cv2.destroyAllWindows()