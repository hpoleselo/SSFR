#!/usr/bin/env python 
import sys
import os
import numpy as np
import cv2
import cv2.aruco as aruco
import glob
import rospy
from geometry_msgs.msg import Point

class ArucoInterface(object):

    def __init__(self):
        # Size of the ArUco marker in meters
        self.marker_size = 0.05
        rospy.init_node("aruco_position_publisher")
        self.positionPublisher = rospy.Publisher("marker_position", Point, queue_size=1)

    def checkCamera(self):
        """ Checks if the camera is available """
        cameraFound = False
        print("[INFO]: Searching for camera...")
        try:
            for camera in glob.glob("/dev/video?"):
                if camera == "/dev/video2":
                    cameraIndex = 2
                    cameraFound = True
                    print("[INFO]: Using index 2 for the camera.")
                    return cameraIndex, cameraFound
                elif camera == "/dev/video1":
                    cameraIndex = 1
                    cameraFound = True
                    print("[INFO]: Using index 1 for the camera.")
                    return cameraIndex, cameraFound
                elif camera == "/dev/video0":
                    cameraIndex = 0
                    cameraFound = True
                    print("[INFO]: Using index 0 for the camera")
                    return cameraIndex, cameraFound
                else:
                    print("[ERROR]: No camera found.")
                    cameraFound = False
                    cameraIndex = 0
                    return cameraIndex, cameraFound
        except(TypeError):
            print("[ERROR]: Camera is probably not connected.")

    def extract_calibration(self):
        """ Gets the the camera and distortion matrix from the calibrate_camera method. By reading the yaml file. """
        #TODO add function to check if the folder exists because opencv points to other error rather than saying it doesnt exist
        cv_file = cv2.FileStorage("calib_images/calibration.yaml", cv2.FILE_STORAGE_READ)
        camera_matrix = cv_file.getNode("camera_matrix").mat()
        dist_matrix = cv_file.getNode("dist_coeff").mat()
        print("[INFO]: Extracted camera parameters.")
        cv_file.release()
        return camera_matrix, dist_matrix

    def blockPrint(self):
        """ function to shut the error down from the console: corrupt JPEG data: # extraneous bytes before marker 0x## """
        sys.stdout = open(os.devnull, 'w')

    def track_aruco(self):
        """ Tracks the ArUco Marker in real time. """
        marker_size = self.marker_size

        # Getting the calibrated parameters
        camera_matrix, dist_matrix = self.extract_calibration()
        self.blockPrint()
        cameraIndex, foundCamera = self.checkCamera()
        self.blockPrint()
        cap = cv2.VideoCapture(cameraIndex)

        while (True and foundCamera):
            # Getting a frame from video stream
            ret, frame = cap.read()
            # Since we are getting BGR frames we have to convert them
            self.blockPrint()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_100)
            parameters = aruco.DetectorParameters_create()

            # Lists of ids and the corners belonging to each id
            corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
            #font = cv2.FONT_HERSHEY_SIMPLEX

            #  Just enters this condition if any id is found on the camera frame
            if np.all(ids is not None):
                self.blockPrint()
                rvec, tvec = aruco.estimatePoseSingleMarkers(corners[0], marker_size, camera_matrix, dist_matrix)
                #(rvec-tvec).any() # get rid of that nasty numpy value array error
                #print 'Rotation Vector: ', rvec
                #print 'Translation Vector:', tvec
                #aruco.drawAxis(frame, camera_matrix, dist_matrix, rvec[0], tvec[0], 0.1)
                #aruco.drawDetectedMarkers(frame, corners)
                #cv2.putText(frame, "Id: " + str(ids), (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)
                
                msgToPublish = Point()
                msgToPublish.x = tvec[0][0][0]
                msgToPublish.z = tvec[0][0][2]
                self.positionPublisher.publish(msgToPublish)
                # If we were not to use ROS:
                #print(tvec[0][0][0])
                #yield tvec[0][0][0]
            
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()



                # Display the resulting frame
                #cv2.imshow('ArucoDetection', frame)
                
            #cap.release()
            #cv2.destroyAllWindows()



ai = ArucoInterface()
ai.track_aruco()


"""
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('[WARN]: Program interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
"""