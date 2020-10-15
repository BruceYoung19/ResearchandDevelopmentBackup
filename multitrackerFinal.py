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
from datetime import datetime
import re
import math

class Tracker:
	#coordinate / bounding boxes
	#actual tracker
	def __init__(self):
		self.tracker = None
	def initCSRT(self, frame, b):
		self.boxes = [b]
		self.startBox = b
		self.tracker = cv2.TrackerCSRT_create()
		self.tracker.init(frame,self.boxes[0])
	def initGOTURN(self, frame, b):
		self.boxes = [b]
		self.startBox = b
		self.tracker = cv2.TrackerGOTURN_create()
		self.tracker.init(frame, self.boxes[0])
	def initMOSSE(self, frame, b):
		self.boxes = [b]
		self.startBox = b
		self.tracker = cv2.TrackerMOSSE_create()
		self.tracker.init(frame, self.boxes[0])
	def initKCF(self, frame, b):
		self.boxes = [b]
		self.startBox = b
		self.tracker = cv2.TrackerKCF_create()
		self.tracker.init(frame,self.boxes[0])
	def updateTracker(self, frame):
		success, box = self.tracker.update(frame)
		if success:
			self.boxes.append(box)
		return (success,box)
	def identity(self):
		return str(self.startBox)
	def drawLine(self):
		midpoints = []
		for b in self.boxes:
			x = int(b[0] + (b[2] / 2))
			y = int(b[1] + (b[3] / 2))
			midpoints.append((x,y))
		return midpoints

class main:
#	box = [(250, 782, 125, 296)]
	box = [(250, 782, 125, 296),(1449, 35, 92, 163), (879, 70, 65, 164), (1651, 123, 64, 158), (715, 238, 66, 172), (1608, 609, 111, 249), (803, 255, 54, 166), (1800, 184, 67, 168), (871, 390, 113, 182), (983, 3, 51, 123),(1349, 19, 56, 109), (1567, 910, 153, 170), (1159, 0, 37, 76), (282, 277, 84, 198), (907, 479, 120, 157)]
	#new bounding boxes dictionary
	newBoxes = {}

	#open text file line by line for new bounding boxes
	textFile = open("newBB.txt","r")
	for line in textFile:
		key = None
		value = []
		x = line.split("-")
		for i in x:
			if(key is None):
				key = int(i)
			else:
				value.append(int(i))
		newBoxes[key] = tuple(value)
	textFile.close()


	# Set video to load
	videoPath = "TownCentreXVID.avi"

	# Create a video capture object to read videos
	cap = cv2.VideoCapture(videoPath)
	
	#frame size for the video
	frame_width = int(cap.get(3))
	frame_height = int(cap.get(4))
	
	#creating a video output file.
	codec = cv2.VideoWriter_fourcc(*'DIVX')
	out = cv2.VideoWriter('output.mp4', codec, 60.0, (frame_width,frame_height))

	#fourcc = cv2.VideoWriter_fourcc(*'mp4v')
	# out = cv2.VideoWriter('test.mp4',fourcc,60,(320,240))
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
	#for the heatmap
	lines = []

	for i in box:
		t = Tracker()
		trackers.append(t)
		t.initMOSSE(frame, i)

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
			fps = FPS().start()
			flag = True
			

		if frameNo in newBoxes:
			t = Tracker()
			trackers.append(t)
			t.initMOSSE(frame, newBoxes[frameNo])

		updatedBoxes = []
		count = 0
		# get updated location of objects in subsequent frames
		for i in trackers:
			trackSuccess, box = i.updateTracker(frame)
			updatedBoxes.append(box)
			if(trackSuccess == False):
				lines.append(trackers[count].drawLine())
				del trackers[count]
			count+=1

		
		# update the FPS counter
		fps.update()
		fps.stop()

		pid = os.getpid()
		py = psutil.Process(pid)
		# memoryUse = str(py.memory_info()[0]/2.**30) # memory use in GB...I think
		rssUse = "{:.2f}".format(py.memory_info()[0]/1048576 ) #memory in megabytes
		vmsUse = "{:.2f}".format(py.memory_info()[1]/1048576 )

		# file.write("FPS: {:.2f}".format(fps.fps())+" - ");
		file.write ("rss memory use:"+ rssUse + "\n")
		file.write ("vms memory use:"+ vmsUse + "\n\n")
		# file.write("Boundary Boxes : " + str(box)+ "\n")

		# draw tracked objects
		if success:
			text = "Frame: "+str(frameNo)
			cv2.putText(frame, text, (10, 1000),
				cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
			count = 0
			for box in updatedBoxes:
				if(len(trackers) > count):
					identity = trackers[count].identity()
				(x, y, w, h) = [int(v) for v in box]
				cv2.rectangle(frame, (x, y), (x + w, y + h),(0, 255, 0), 2)
				cv2.putText(frame, identity, (x, y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
				count+=1
			for l in lines:
				size = len(l)
				for i in range(size-1):
					cv2.line(frame, l[i],l[i+1],(0, 255, 0), 2)

		# show frame
		# cv2.imshow('MultiTracker', frame)
		print(frameNo)
		out.write(frame)
		# quit on ESC button
		if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
			break

	#end timer
	end = time.time();
	timeSec = end - start;
	timeMin = str(timeSec/60);

	print("time elasped: "+ str(timeSec) +"seconds - "+timeMin+" minutes.");
	# close all windows
	cv2.destroyAllWindows()

