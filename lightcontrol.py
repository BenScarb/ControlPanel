#!/usr/bin/python
import time
import random
import datetime

from neopixel import *

class Lights(object):
    def __init__(self):
        # LED strip configuration:
        self.LED_COUNT      = 15      # Number of LED pixels.
        self.LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
        self.LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
        self.LED_BRIGHTNESS = 10      # Set to 0 for darkest and 255 for brightest
        self.LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
        self.strip = None
        self.Colours = dict()
        self.Colours['Red'] = Color(0, 255, 0)
        self.Colours['Green'] = Color(255, 0, 0)
        self.Colours['Blue'] = Color(0, 0, 255)
        self.Colours['White'] = Color(255, 255, 255)
        self.Colours['Off'] = Color(0, 0, 0)
        self.Colours['On'] = Color(255, 255, 255)
        self.Terminate = False
        self.Running = False

    def _WaitForStop(self):
        while self.Running:
            time.sleep(1)

    def CreateStrip(self):
        # Init the strip to the desired values
        self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

    def _TurnOn(self, color):
        # Turn the whole strip on
        for led in range(self.strip.numPixels()):
                self.strip.setPixelColor(led, color)
        self.strip.show()

    def TurnOff(self):
        self.Terminate = True
        self._WaitForStop()
        self.Terminate = False
        self.Running = True
        self._Clear()
        self.Running = False

    def _Clear(self, do_show = True):
        for led in range(self.strip.numPixels()):
                self.strip.setPixelColor(led, 0)
        if do_show:
            self.strip.show()

    def _ColorWipe(self, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def _Cyclon(self, red, green, blue, eye_size, speed_delay, return_delay):
        eye_color = Color(blue, red, green)
        reduced_color = Color(blue/10, red/10, green/10)

        for i in range(self.strip.numPixels()):
            self._Clear(False)
            self.strip.setPixelColor(i, reduced_color)
            for j in range(0, eye_size):
                self.strip.setPixelColor(i+j, eye_color)
            self.strip.setPixelColor(i + eye_size, reduced_color)
            self.strip.show()
            time.sleep(speed_delay)

        time.sleep(return_delay)

        for i in range(self.strip.numPixels(), 0-eye_size, -1):
            self._Clear(False)
            self.strip.setPixelColor(i, reduced_color)
            for j in range(0, eye_size):
                self.strip.setPixelColor(i+j, eye_color)
            self.strip.setPixelColor(i + eye_size, reduced_color)
            self.strip.show()
            time.sleep(speed_delay)

    def _PositiveRun(self, color, size, speed):
        for led in range(self.strip.numPixels()):
            self._Clear(False)
            for led_light in range(size):
                self.strip.setPixelColor(led+led_light, color)
            self.strip.show()
            time.sleep(speed)

    def _NegativeRun(self, color, size, speed):
        for led in range(self.strip.numPixels(), -size, -1):
            self._Clear(False)
            for led_light in range(size):
                self.strip.setPixelColor(led+led_light, color)
            self.strip.show()
            time.sleep(speed)

    def OnForTime(self, color, on_time):
        self.Terminate = True
        self._WaitForStop()
        self.Terminate = False
        self.Running = True
        on_time = int(on_time)
        if time == -1:
            self._TurnOn(color)
        else:
            self._TurnOn(color)
            start_time = datetime.datetime.now()
            while ((datetime.datetime.now()-start_time).total_seconds() < on_time) and not self.Terminate:
                time.sleep(1)
            self._Clear()
        self.Running = False

    def ToShedForTime(self, color, on_time):
        self.Terminate = True
        self._WaitForStop()
        self.Terminate = False
        self.Running = True
        on_time = int(on_time)
        if time == -1:
            while not self.Terminate:
                self._NegativeRun(color, 4, 0.05)
        else:
            start_time = datetime.datetime.now()
            while ((datetime.datetime.now()-start_time).total_seconds() < on_time) and not self.Terminate:
                self._NegativeRun(color, 4, 0.05)
            self._Clear()
        self.Running = False

    def ToHouseForTime(self, color, on_time):
        self.Terminate = True
        self._WaitForStop()
        self.Terminate = False
        self.Running = True
        on_time = int(on_time)
        if time == -1:
            while not self.Terminate:
                self._PositiveRun(color, 4, 0.05)
        else:
            start_time = datetime.datetime.now()
            while ((datetime.datetime.now()-start_time).total_seconds() < on_time) and not self.Terminate:
                self._PositiveRun(color, 4, 0.05)
            self._Clear()
        self.Running = False

# Main program logic follows:
if __name__ == '__main__':
    lights = Lights()
    lights.CreateStrip()
    lights._Clear()
    # for i in range(5):
    #     lights.Cyclon(255, 0, 0, 3, 0.05, 0.1)
    for i in range(5):
        lights._NegativeRun(lights.Colours["Red"], 3, 0.1)
    print('Press Ctrl-C to quit.')
    try:
        waitTime = 0.05
        reduceBy = -0.05
        while True:
            #spin(strip, 1, waitTime, random.choice(myCols))
            print("ColourWipe")
            colour = random.choice(list(lights.Colours.keys()))
            lights._ColorWipe(lights.Colours[colour], 10)

            if waitTime <= 0.1:
                    reduceBy = 0.05
            elif waitTime >= 0.25:
                    reduceBy = -0.05
            waitTime += reduceBy
    except KeyboardInterrupt:
            pass
    finally:
            lights._Clear()
