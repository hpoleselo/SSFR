#!/usr/bin/env python 
import sys
import os
import numpy as np
import cv2
import cv2.aruco as aruco
import glob

class ArucoInterface(object):

    def __init__(self):
        # Size of the ArUco marker in meters
        self.marker_size = 0.05

    def checkCamera(self):
        """ Checks if the camera is available """
        cameraFound = False
        for camera in glob.glob("/dev/video?"):
            if camera == "/dev/video2":
                cameraIndex = 2
                cameraFound = True
                return cameraIndex, cameraFound
            elif camera == "/dev/video1":
                cameraIndex = 1
                cameraFound = True
                return cameraIndex, cameraFound
            else:
                print("[ERROR]: No camera found.")
                cameraFound = False
                cameraIndex = 0
                return cameraIndex, cameraFound

    def extract_calibration(self):
        """ Gets the the camera and distortion matrix from the calibrate_camera method. By reading the yaml file. """
        cv_file = cv2.FileStorage("calib_images/calibration.yaml", cv2.FILE_STORAGE_READ)
        camera_matrix = cv_file.getNode("camera_matrix").mat()
        dist_matrix = cv_file.getNode("dist_coeff").mat()
        print("[INFO]: Extracted camera parameters.")
        cv_file.release()
        return camera_matrix, dist_matrix

    def track_aruco(self):
        """ Tracks the ArUco Marker in real time. """
        marker_size = self.marker_size

        # Getting the calibrated parameters
        camera_matrix, dist_matrix = self.extract_calibration()              
        cameraIndex, foundCamera = self.checkCamera()

        cap = cv2.VideoCapture(cameraIndex)
        
        while (True and foundCamera):
            # Getting a frame from video stream
            ret, frame = cap.read()

            # Since we are getting BGR frames we have to convert them
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_100)
            parameters = aruco.DetectorParameters_create()

            # Lists of ids and the corners belonging to each id
            corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
            font = cv2.FONT_HERSHEY_SIMPLEX

            #  Just enters this condition if any id is found on the camera frame
            if np.all(ids is not None):
                rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners[0], marker_size, camera_matrix, dist_matrix)
                #(rvec-tvec).any() # get rid of that nasty numpy value array error
                #print 'Rotation Vector: ', rvec
                #print 'Translation Vector:', tvec
                aruco.drawAxis(frame, camera_matrix, dist_matrix, rvec[0], tvec[0], 0.1)
                # Drawing a square on the identified marker
                aruco.drawDetectedMarkers(frame, corners)
                ###### Draw ID on the screen #####
                cv2.putText(frame, "Id: " + str(ids), (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)
                print(tvec)
                # Only get the x position of the marker
                #return tvec[0][0][0]


            # Display the resulting frame
            cv2.imshow('ArucoDetection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        #cap.release()
        #cv2.destroyAllWindows()


def main():
    arucao = ArucoInterface()
    arucao.track_aruco()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('[WARN]: Program interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
