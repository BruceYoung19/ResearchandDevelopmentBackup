from __future__ import print_function
import sys
import cv2
from random import randint
import platform
import datetime
import os
import numpy as np
import psutil #for keeping track of OS
import time #keeping track of system time
from imutils.video import FPS
from datetime import datetime

#MultiTracker Class
class MultiTracker:
	def init():
		tr = Tracker

class Tracker:
	#coordinate / bounding boxes
	#actual tracker
	def initGOTURN(frame, box):
		global tracker
		bb = box
		tracker = cv2.TrackerGOTURN_create()
		tracker.init(frame,box)
		return tracker
	def initMOSSE(frame, box):
		global tracker
		bb = box
		tracker = cv2.TrackerMOSSE_create()
		tracker.init(frame,box)
		return tracker
	def initKCF(frame, box):
		global tracker
		bb = box
		tracker = cv2.TrackerKCF_create()
		tracker.init(frame,box)
		return tracker
	def initCSRT(frame, box):
		global tracker
		bb = box
		tracker = cv2.TrackerCSRT_create()
		tracker.init(frame,box)
		return tracker
	def update(track, frame):
		return (track.update(frame))

class main:
	box = [(250, 782, 125, 296), (1449, 35, 92, 163), (879, 70, 65, 164), (1651, 123, 64, 158), (715, 238, 66, 172),
		   (1608, 609, 111, 249), (803, 255, 54, 166), (1800, 184, 67, 168), (871, 390, 113, 182), (983, 3, 51, 123),
		   (1349, 19, 56, 109), (1567, 910, 153, 170), (1159, 0, 37, 76), (282, 277, 84, 198), (907, 479, 120, 157)]

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

	now = datetime.now()
	dtStr = now.strftime("%d.%m.%Y_%H.%M")
	filename = dtStr+".txt"
	# Writing a file
	file = open(filename,"w")

	# writing system requirements
	file.write("Machine (Bit): " + platform.machine() + "\n")
	file.write("Machine - Version: " + platform.version() +" \n")
	file.write("Machine - Platform: " + platform.platform() + "\n")
	file.write("Machine - System: " + platform.system()+ "\n")

	psutil.virtual_memory()
	file.write("Virtual Memory - Avaliable : "  + str(psutil.virtual_memory().percent) + "\n")

	
	#initialise tracker
	trackers = []

	t = Tracker
	for i in box:
		trackers.append(t.initKCF(frame, i))

	#start timer
	start = time.time()

	#flag for fps counter
	flag = False

	frameNo = -1
	# Process video and track objects
	while cap.isOpened():
		frameNo += 1
		success, frame = cap.read()
		if not success:
			break
		if success and not flag:
			out.write(frame)
			fps = FPS().start()
			flag = True

		if frameNo == 5:
			print("NEW BOX")
			trackers.append(t.initKCF(frame, (639, 988, 148, 86)))

		boxes = []
		# get updated location of objects in subsequent frames
		for i in trackers:
			trackSuccess, box = t.update(i, frame)
			boxes.append(box)

		# update the FPS counter
		fps.update()
		fps.stop()

		pid = os.getpid()
		py = psutil.Process(pid)
		# memoryUse = str(py.memory_info()[0]/2.**30) # memory use in GB...I think
		rssUse = str(py.memory_info()[0]) #memory in bytes
		vmsUse = str(py.memory_info()[1])

		# file.write("FPS: {:.2f}".format(fps.fps())+" - ");
		file.write ("rss memory use:"+ rssUse + "\n")
		file.write ("vms memory use:"+ vmsUse + "\n")
		# file.write("Boundary Boxes : " + str(box)+ "\n")

		# draw tracked objects
		if success:
			for box in boxes:
				(x, y, w, h) = [int(v) for v in box]
				cv2.rectangle(frame, (x, y), (x + w, y + h),(0, 255, 0), 2)
		# for i, newbox in enumerate(boxes):
		# 	p1 = (int(newbox[0]), int(newbox[1]))
		# 	p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
		# 	cv2.rectangle(frame, p1, p2, (0, 255, 0), 2, 1)

		
		# show frame
		cv2.imshow('MultiTracker', frame)

		# quit on ESC button
		if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
			break

	#end timer
	end = time.time();
	timeSec = end - start;
	timeMin = str(timeSec/60);

	print("time elasped: "+ str(timeSec) +"seconds - "+timeMin+" minutes.");
	# close all windows
	out.release()
	cv2.destroyAllWindows()

