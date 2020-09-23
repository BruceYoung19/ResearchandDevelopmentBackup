# import the necessary packages
#include <opencv2/tracking/tracker.hpp>
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils

import time
import cv2

tracker = cv2.TrackerGOTURN_create()  

# Read video
video = cv2.VideoCapture("TownCentreXVID.avi")

# Exit if video not opened
if not video.isOpened():
    print("Could not open video")
    sys.exit()

# Read first frame
ok,frame = video.read()
if not ok:
    print("Cannot read video file")
    sys.exit()

bbox = (276, 23, 86, 320)

ok = tracker.init(frame,bbox)

while True:
    # Read a new frame
    ok, frame = video.read()
    if not ok:
        break

    # Start timer
    timer = cv2.getTickCount()

    # Update tracker
    ok, bbox = tracker.update(frame)

    # Calculate Frames per second (FPS)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

    # Draw bounding box
    if ok:
        # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
    else :
        # Tracking failure
        cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

    # Display tracker type on frame
    cv2.putText(frame, "GOTURN Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);

    # Display FPS on frame
    cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

    # Display result
    cv2.imshow("Tracking", frame)
 
    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break
