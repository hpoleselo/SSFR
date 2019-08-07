import sys
import os
import numpy as np
import cv2
import glob
import cv2.aruco as aruco


class ArucoInterface(object):

    # If you want to see the pictures slowly then just change the WAIT_TIME
    def __init__(self, wait_time=10 , chessb_col=9, chessb_row=6):

        # Our chessboard is composed by 10 rows and 6 columns! Which only 9x6 corners would be detected

        self.wait_time = wait_time
        self.chessb_col = chessb_col
        self.chessb_row = chessb_row
        # Path for loading the images
        self.load_image = 'calib_images/*.jpg'
        # Termination criteria
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        # Size of the ArUco marker in meters
        self.marker_size = 0.05

    def extract_calibration(self):
        ''' Gets the the camera and distortion matrix from the calibrate_camera method. By reading the yaml file.'''
        cv_file = cv2.FileStorage("calib_images/calibration.yaml", cv2.FILE_STORAGE_READ)
        #print 'Type from read file:', type(cv_file)
        # Note we also have to specify the type to retrieve other wise we only get a
        # FileNode object back instead of a matrix

        camera_matrix = cv_file.getNode("camera_matrix").mat()
        dist_matrix = cv_file.getNode("dist_coeff").mat()
        print("Extracted camera parameters.")
        cv_file.release()
        return camera_matrix, dist_matrix

    def track_aruco(self):
        ''' Tracks the ArUco Marker in real time. '''
        chessb_col = self.chessb_col
        chessb_row = self.chessb_row
        load_image = self.load_image
        criteria = self.criteria
        marker_size = self.marker_size

        # Getting the calibrated parameters
        camera_matrix, dist_matrix = self.extract_calibration()

        # Get video stream from camera source
        cap = cv2.VideoCapture(1)
        
        # Implement exception handling for opening the camera
        # check for lsusb and logitech ls /dev/video1
            #print("Could not find the camera connected, check if the index is correct or if the camera is connected.")
            #print("$ lsusb or $  ")
            #sys.exit()
        
        while (True):
            # Getting a frame from video stream
            ret, frame = cap.read()

            # Since we are getting BGR frames we have to convert them
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Later try to use own dictionary to generate less markers since we dont need too much
            aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_100)
            parameters = aruco.DetectorParameters_create()

            # Lists of ids and the corners belonging to each id
            corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
            font = cv2.FONT_HERSHEY_SIMPLEX

            # Checks before if all the values on the matrix are different than None
            if np.all(ids != None):
                # Estimate pose of each marker and return the values rvet and tvec, NOTE THAT those are DIFFERENT from camera coefficents
                # The second parameter is the size of the marker in meters
                # The length of these vectors are just one, meaning they have 3 columns but just one row! And they store the real pose value
                rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners[0], marker_size, camera_matrix, dist_matrix)
                #(rvec-tvec).any() # get rid of that nasty numpy value array error
                #print 'Rotation Vector: ', rvec
                #print 'Translation Vector:', tvec
                aruco.drawAxis(frame, camera_matrix, dist_matrix, rvec[0], tvec[0], 0.1)
                # Drawing a square on the identified marker
                aruco.drawDetectedMarkers(frame, corners)

                ###### Draw ID on the screen #####
                cv2.putText(frame, "Id: " + str(ids), (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)

                # Only get the x position of the marker
                return tvec[0][0][0]


            # Display the resulting frame
            cv2.imshow('ArucoDetection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # Maybe add a method that exits and we can call it on the main method 
        cap.release()
        cv2.destroyAllWindows()


def main():
    arucao = ArucoInterface()
    arucao.track_aruco()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)