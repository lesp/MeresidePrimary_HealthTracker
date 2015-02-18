
# Activity Monitor by Mereside Primay School#
# Sources of libraries and code used in this project are credited below

# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

# ADXL345 Python example 
#
# author:  Jonathan Williamson
# license: BSD, see LICENSE.txt included in this package
# 
# This is an example to show you how to use our ADXL345 Python library
# http://shop.pimoroni.com/products/adafruit-triple-axis-accelerometer


import time
import math
from neopixel import *
from adxl345 import ADXL345
import RPi.GPIO as GPIO


# LED strip configuration:
LED_COUNT      = 12      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 30      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

     

def displayCurrentActivity(strip, accelerometer, cumulativeActivity):
        """Vary pixel 11 based on current accelerometer activity"""
        currentActivity = 0        
        for i in range (5):
                axes = accelerometer.getAxes(True)
                activity1 = abs(axes['x']) + abs(axes['y']) + abs(axes['z'])
                time.sleep(0.03);
                axes = accelerometer.getAxes(True)
                activity2 = abs(axes['x']) + abs(axes['y']) + abs(axes['z'])
                currentActivity =+ abs(activity1 - activity2)
                time.sleep(0.03);
                
        currentActivity *= 10
        if (currentActivity > 25):
                currentActivity = 25
                
        
        if (currentActivity < 0.6):
                strip.setPixelColor(10, Color(254, 0, 0))
        else:
                blue = int((abs(20 - currentActivity) / 24) * 255)
                if (blue > 250):
                        blue = 255
                elif (blue < 0):
                        blue = 0
                        
                green = int((currentActivity / 15) * 255)
                if (green > 255):
                        green = 255
                elif (green < 0):
                        green = 0
      
                strip.setPixelColor(10, Color(0, green, blue))
        strip.show()

        if (currentActivity > 8):
                cumulativeActivity += 0.6

        return cumulativeActivity
                
def displayCurrentHeart(strip):
        """Vary pixel 0 based on current heart activity"""
        if ((GPIO.input(14) == 0) & (GPIO.input(15) == 0)):
                strip.setPixelColor(11, Color(0, 0, 255))
        if ((GPIO.input(14) == 1) & (GPIO.input(15) == 0)):
                strip.setPixelColor(11, Color(0, 155, 0))
        if ((GPIO.input(14) == 0) & (GPIO.input(15) == 1)):
                strip.setPixelColor(11, Color(255, 0, 0))
        if ((GPIO.input(14) == 1) & (GPIO.input(15) == 1)):
                strip.setPixelColor(11, Color(255, 255, 255))
                

def displayCumulativeActivity(strip, cumulativeActivity):
        """Display cumulative activity across remaining 10 pixels"""

        # Length of time in each segment in seconds
        TIME_SEGMENT = 10

        fullSecondsOfActivity = int(math.floor(cumulativeActivity))  # Floor still returns a float?
        completeTimeSegments = fullSecondsOfActivity / TIME_SEGMENT

        if (completeTimeSegments > 10):
                completeTimeSegments = 10

        for aPixel in range(10):
               strip.setPixelColor(aPixel, Color(0, 0, 255))
               
        for aPixel in range(completeTimeSegments ):
               strip.setPixelColor(aPixel, Color(0, 255, 0))
               
        strip.show()
                
# Main program logic follows:
if __name__ == '__main__':
        # Create NeoPixel object with appropriate configuration.
        strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        # Intialize the library (must be called once before other functions).
        strip.begin()

        # Initialize the Accelerometer
        accelerometer = ADXL345()

        # cumulativeActivity counter
        cumulativeActivity = 0   

        # initialize the GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(14, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(15, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
                
        while True:
                displayCurrentHeart(strip)
                cumulativeActivity = displayCurrentActivity(strip, accelerometer, cumulativeActivity)
                displayCumulativeActivity(strip, cumulativeActivity)
                


