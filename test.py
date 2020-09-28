from __future__ import print_function
import sys
import cv2
from random import randint
import platform
import datetime
import os
import psutil #for keeping track of OS


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
file = open("Test.txt","w")

# writing system requirements
file.write("Machine (Bit): " + platform.machine() + "\n")
file.write("Machine - Version: " + platform.version() +" \n")
file.write("Machine - Platform: " + platform.platform() + "\n")
file.write("Machine - System: " + platform.system()+ "\n")

## Select boxes
bboxes = [(500,500,50,50)]
# bboxes = [(250, 782, 125, 296), (1449, 35, 92, 163)]

# Create MultiTracker object
multiTracker = cv2.MultiTracker_create()

# Initialize MultiTracker
# for bbox in bboxes:
#   multiTracker.add(kcf_, frame, bbox)
#   print(bbox)
# box = (250, 782, 125, 296)
box = (800, 500, 200, 200)
box2 = (1449, 35, 92, 163)
box3 = (879,70,65,164)
box4 = (1651,123,64,158)

# create a new object tracker for the bounding box and add it
# to our multi-object tracker
tracker = cv2.TrackerKCF_create()
multiTracker.add(tracker, frame, box)

tracker1 = cv2.TrackerKCF_create()
multiTracker.add(tracker1, frame, box2)

tracker2 = cv2.TrackerKCF_create()
multiTracker.add(tracker2, frame, box3)

tracker3 = cv2.TrackerKCF_create()
multiTracker.add(tracker3, frame, box4)
# trackers.add(tracker, frame, box,trackers)

initalTime = datetime.datetime.now()
# Process video and track objects
while cap.isOpened():
	
	success, frame = cap.read()
	if not success:
		break

	# get updated location of objects in subsequent frames
	success, boxes = multiTracker.update(frame)

	pid = os.getpid()
	py = psutil.Process(pid)
	memoryUse = str(py.memory_info()[0]/2.**30) # memory use in GB...I think
	file.write ("memory use:"+ memoryUse + "\n")

	# draw tracked objects
	for i, newbox in enumerate(boxes):
		p1 = (int(newbox[0]), int(newbox[1]))
		p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
		cv2.rectangle(frame, p1, p2, (0, 255, 0), 2, 1)
	# show frame
	cv2.imshow('MultiTracker', frame)

	# quit on ESC button
	if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
		
		FinishTime = datetime.datetime.now()
				
		#overall time
		FinalTime = str(FinishTime - initalTime)
		file.write("Time of executation: " + FinalTime +"\n")
		break
	

# close all windows
cv2.destroyAllWindows()