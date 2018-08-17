#! /usr/bin/python

from fractions import Fraction
from skimage import io, img_as_float
from picamera import PiCamera
from time import sleep
import numpy    as np
import openpyxl as xl
import serial
import os

IT = "IT"
IO = "IO"
TRANSMITTANCE = "TRANSMITTANCE"
ABSORBANCE    = "ABSORBANCE"


def test():
    print str(np.mean(rgb2gray(capture('test.png'))))

def main():
    global camera, ser

    camera = PiCamera(           # Camera Object
        resolution=(1024,720),   # Resolution 1024 x 720
        framerate=Fraction(1,6), # 1/6 fps
        sensor_mode=3)           # Long Exposure Mode

    ser = serial.Serial(
        port='/dev/ttyUSB0', # Open Serial Port
        baudrate=9600)      # baudrate

    print ser.name # Print serial name to console.

    print """
        This program measures uses a pi cam to measure the intensity
        of light passing through a sample in the spectrophotometer.
        
        Please enter a sample name. The data will be exported to an
        Excel spreadsheet named after the sample.
        """
    
    sample_name = raw_input()
   
    print """
        First, place a blank sample to create a baseline for input intensity.
        When the sample is in place, press any key to continue.
        """
    
    raw_input() # Wait for user input.
    
    it = scan(IT) # Get Intensity In.
    
    print it

    print """
        The baseline scan is complete. Place the next sample for scanning.
        When done, press any key to continue. 
        """
        
    
    raw_input() # Wait for user input.
    
    io = scan(IO) # Get Intensity out

    print io

    print "Exporting to Spreadsheet"
    send2xl(sample_name, it, io)



    # Shutdown
    ser.close()


def scan(flag='scan'):
    # empty data set.
    data = []
    for i in range(51):
        print "Measuring wavelength %d" % ustep2wl(i)
        send2serial(str(i)) # Moves grating to microstep i.
        data.append(np.mean(rgb2gray(capture("./%s_%s.png" % (flag, ustep2wl(i))))))
    return data

# Microstep Overstep

def send2serial(microstep):
    if not ser.is_open: ser.open()
    ser.write(microstep)
    

# Microstep to Wavelength.
def ustep2wl(ustep):
    return 700 - ustep * 6.2

# Camera
def capture(imgdst):

    # Defined in main()
##    camera = PiCamera(
##        resolution=(1024,720),
##        framerate=Fraction(1,6), # 1/6 fps
##        sensor_mode=3) # Long Exposure Mode

    camera.shutter_speed = 6000000 # 6 seconds
    camera.iso = 800 # Maximum gain

    sleep(30) # Gives picam time to set gains and measure AWB
    camera.exposure_mode = 'off'
    
    camera.capture(imgdst) # Take picture. 

    img = io.imread(imgdst) # Open img as numpy array. 
    img = img_as_float(img) # Make float for processing.
    
    return img
    

# Grayscale
def rgb2gray(rgb):
    # Return grayscale intensity map.
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])


# Manage Excel Sheet.
def send2xl(wbNameStr, it, io):
    wb = xl.Workbook()       # Create new Excel file.
    sheet = wb.active        # Edit first sheet.
    sheet.title = "Sample_1" # Change to default name of Sample_1
    sheet["A1"] = "Wavelength"          #A1
    sheet["B1"] = "Intensity in (It)"   #B1
    sheet["C1"] = "Intensity out (Io)"  #C1
    sheet["D1"] = "Transmittance"       #D1
    sheet["E1"] = "Absorbance"          #E1
    
    # Data Entry
    for i in range(50):
        sheet["A%d" % i+1] = str(ustep2wl(i)) # Wavelength.
        sheet["B%d" % i+1] = str(it[i]) # Intensity In,  Column A.
        sheet["C%d" % i+1] = str(io[i]) # Intensity Out, Column B
        sheet["D%d" % i+1] = "=A%d/B%d" % (i+1, i+1) # Transmittance.
        sheet["E%d" % i+1] = "=LOG(C%d; 10)" % (i+1) # Absorbance.
    
    # Save workbook and return object. 
    wb.save(wbNameStr + '.xlsx' if not wbNameStr.endswith('.xlsx') else '')
    return wb    
    

if __name__ == "__main__":
    main()
    #test()
    
