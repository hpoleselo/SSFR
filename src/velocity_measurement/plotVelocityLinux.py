'''
Reads in data over a serial connection and plots the results live. Before closing, the data is saved to a .txt file.
Modified example originanlly taken from https://www.instructables.com/id/Using-an-Arduino-and-Python-to-plotsave-data/
'''

import serial
import matplotlib.pyplot as plt
import numpy as np


class MeasurementPlotter(object):
    def __init__(self):
        self.connected = False
        # Arduino is set always in linux to /dev/ttyUSB0
        self.ser = serial.Serial('/dev/ttyUSB0', 9600) #sets up serial connection (make sure baud rate is correct - matches Arduino)
        print("Using port: %s") %self.ser.name
        self.checkConnectivity()

    def checkConnectivity(self):
        while not self.connected:
            x = self.ser.read()          # read one byte
            print("Reading one byte: %s") %x
            self.connected = True
            self.graphSetup()

    def graphSetup(self):
        plt.ion()                    #sets plot to animation mode

        # How many points we want to retrieve from the readings
        length = 500

        # Creating the variable before we store the values to be read
        vel = [0]*length

        # Sets up future lines to be modified
        # CHECAR COMO PLOTAR O TEMPO
        #xline = plt.plot(t)
        yline, = plt.plot(vel)

        plt.ylim(400,700)   # Sets the y axis limits
        # Closes serial connection (very important to do this! if you have an error partway through the code, type this into the cmd line to close the connection)  
        self.ser.close()

MeasurementPlotter()

def readSerialValues(self):
    # This will parse through length and read the serial values
    for i in range(length):
        data = self.ser.readline()    # Reads until it gets a carriage return. MAKE SURE THERE IS A CARRIAGE RETURN OR IT READS FOREVER
        separate = data.split()      # Splits string into a list at the tabs
        #print separate
    
        vel.append(int(separate[0]))   #add new value as int to current list
    
        del vel[0]
    
        #xline.set_xdata(np.arange(len(x))) #sets xdata to new list length
        yline.set_ydata(np.arange(len(vel)))
    
        plt.pause(0.001)                   #in seconds
        plt.draw()                         #draws new plot

def saveData(self):
    rows = zip(vel, t)                  #combines lists together

    row_arr = np.array(rows)               #creates array from list
    np.savetxt("C:\\Users\\mel\\Documents\\Instructables\\test_radio2.txt", row_arr) #save data in file (load w/np.loadtxt())
