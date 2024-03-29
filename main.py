# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# in order to run the 
# sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
# Simple test for NeoPixels on Raspberry Pi
# https://learn.adafruit.com/adafruit-neopixel-uberguide/python-circuitpython
import time
import board
import neopixel
import threading
from datetime import datetime
from gpiozero import Button
from signal import pause
#Setup the pin
#GPIO.setmode(GPIO.BOARD)
buttonPin = 16 # board.D23
button = Button(23)

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 50
led_pattern = 0

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER
)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

# alternating between rainbow and red
def setRunningLightTrack(count, rgb):
    for i in range(num_pixels):
        interval = count % 3
        if (i + interval) % 3 == 0:
            pixels[i] = rgb
        else:
            pixels[i] = (0, 0, 0)
    pixels.show()

# alternating between rainbow and red
def redLightTrack():
    global endLedEffect
    for seconds in range(3600):
        if endLedEffect == True:
            print('cancel the LED effect early')
            pixels.fill((0, 0, 0))   
            pixels.show()
            endLedEffect = False
            return
        setRunningLightTrack(seconds, (255, 0, 0))
        pixels.show()
        time.sleep(0.125)

def blueLightTrack():
    global endLedEffect
    for seconds in range(3600):
        if endLedEffect == True:
            print('cancel the LED effect early')
            pixels.fill((0, 0, 0))   
            pixels.show()
            endLedEffect = False
            return
        setRunningLightTrack(seconds, (0, 0, 255))
        pixels.show()
        time.sleep(0.125)
        
def greenLightTrack():
    global endLedEffect
    for seconds in range(3600):
        if endLedEffect == True:
            print('cancel the LED effect early')
            pixels.fill((0, 0, 0))   
            pixels.show()
            endLedEffect = False
            return
        setRunningLightTrack(seconds, (0, 255, 0))
        pixels.show()
        time.sleep(0.125)
        
# track lighting move the leds blank 2 one on moving.

def setPixelDecimal(countingNumber, pixelOffset, numberOfPixels, rgb):
     for secondsIndex in range(pixelOffset, pixelOffset + numberOfPixels):
            
            if(countingNumber > (secondsIndex - pixelOffset)):
                pixels[secondsIndex] = rgb
            else:
                pixels[secondsIndex] = (0, 0, 0)

def setTimeInPixels(totalSeconds):
    totalSeconds = totalSeconds // 1
    print('printing the current time.')
    secondsOffset = 0 # 0 through 9
    tensOfSecondsOffset = 11 # 11 through 16
    minutesOffset = 18 # 18 through 29
    tensOfMinutesOffset = 31 # 31 through 36
    hoursOffset = 38 # 38 through 47 
    tensOfHoursOffset = 48 # 48 through 50
    # number of seconds in a day.

    #hours
    hours = totalSeconds // 3600
    minutes = totalSeconds // 60
    seconds = totalSeconds % 10
    tensOfSeconds = (totalSeconds % 60) // 10
    tensOfMinutes = (minutes % 60) // 10
    minutes = minutes % 10
    tensOfHours = hours // 10
    hours = hours % 10  
    print(f'{tensOfHours}{hours}:{tensOfMinutes}{minutes}:{tensOfSeconds}{seconds}')

    # seconds
    setPixelDecimal(seconds, secondsOffset, 10, (255, 255, 0))
    setPixelDecimal(tensOfSeconds, tensOfSecondsOffset, 6, (0, 255, 0))
    
    # Minutes
    setPixelDecimal(minutes, minutesOffset, 10, (0, 255, 255))
    setPixelDecimal(tensOfMinutes, tensOfMinutesOffset, 6, (0, 0, 255))
    
    # hours
    setPixelDecimal(hours, hoursOffset, 10, (255, 0, 255))
    setPixelDecimal(tensOfHours, tensOfHoursOffset, 2, (255, 0, 0))
    
    pixels.show()

def currentTime():
    global endLedEffect
    print('Current time ')
    currentTime = datetime.now()
    # number of seconds in a day.
    while endLedEffect != True:
        currentTime = datetime.now()
        seconds_since_midnight = (currentTime - currentTime.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
        setTimeInPixels(seconds_since_midnight)
        time.sleep(1)
    pixels.fill((0,0,0))
    pixels.show()
    endLedEffect = False


def countingLed():
    global endLedEffect
    print('Counting LEDs')
    # number of seconds in a day.
    for totalSeconds in range(86400):
        if endLedEffect == True:
            print('cancel the clock Effect early')
            pixels.fill((0, 0, 0))   
            pixels.show()
            endLedEffect = False
            return

        setTimeInPixels(totalSeconds)
        time.sleep(1)
    pixels.fill((0, 0, 0))
    pixels.show()


ledThread = threading.Thread(name='LedThread')
endLedEffect = False

def ledRainbow():
    global endLedEffect
    for x in range(3600):
        # check to see if we have aborted the thread
        if endLedEffect == True:
            print('cancel the LED effect early')
            pixels.fill((0, 0, 0))   
            pixels.show()
            endLedEffect = False
            return
        rainbow_cycle(0.001)
        print(x)
        pixels.show()
    # turn off the LEDs
    pixels.fill((0, 0, 0))
    pixels.show()

def slowLedRainbow():
    global endLedEffect
    for x in range(3600):
        # check to see if we have aborted the thread
        if endLedEffect == True:
            print('cancel the LED effect early')
            pixels.fill((0, 0, 0))   
            pixels.show()
            endLedEffect = False
            return
        rainbow_cycle(0.01)
        print(x)
        pixels.show()
    # turn off the LEDs
    pixels.fill((0, 0, 0))
    pixels.show()


def ledFadeRed():
    global endLedEffect
    print('LED Fade up and down')
    for numberOfFades in range(10):
        for x in range(510):
            if endLedEffect == True:
                print('cancel the LED Fade effect early')
                pixels.fill((0, 0, 0))   
                pixels.show()
                endLedEffect = False
                return
            redIn = x
            if x > 255:
                redIn = 510 - x
            print('red: ')
            print(redIn)
            pixels.fill((redIn, 0, 0))   
            pixels.show()
            time.sleep(0.01)
        
    # turn off the LEDs
    pixels.fill((0, 0, 0))
    pixels.show()
    
def redBreathingTraining():
    # this pattern will raise at a rate based on https://www.uptodate.com/contents/image/print?imageKey=EM%2F78097
    #
    global endLedEffect 
    age=6
    breathCount=get_breaths_per_min(age)
    # Get the number of milseconds between pulses
    millisecondsPerPulse=60000/breathCount
    # the pattern will rise from one side up to the end of the other side.
    for tenMillisecond in range(0, millisecondsPerPulse, 10):
        # increment by 10 miliseconds
        if endLedEffect == True:
            print('cancel the LED effect early')
            pixels.fill((0, 0, 0))   
            pixels.show()
            endLedEffect = False
            return
        
        setRunningLightTrack(seconds, (255, 0, 0))
    pixels.show()
    time.sleep(0.125)

def set_led_pulse_level(millisecond, millisecondsPerPulse):
    # Based on this paper your inhale to Exhale ratio is 2.33 https://www.thebreathingdiabetic.com/van-diest-et-al-2014
    
    #check if pulse is Inhaling
    inhaleToExhaleRatio=0.429
    totalInhalingTime=millisecondsPerPulse-(millisecondsPerPulse*inhaleToExhaleRatio)
    totalExhalingTime=millisecondsPerPulse-totalInhalingTime
    
    # TODO: potentially add a setting that would represent the led color associated with the blood color
    # start out blue at the begining of inhale to red at the beginning of exhale
    isInhaling=True
    if(millisecond < (millisecondsPerPulse*inhaleToExhaleRatio)):
        isInhaling=False
    
    # determine what percentage they have completed of the inhale or exhale
    currentRelativeTime = millisecond
    percentage = millisecond/totalExhalingTime
    if(isInhaling):
        currentRelativeTime = millisecond-totalExhalingTime
        percentage = currentRelativeTime/totalInhalingTime
    
    # set the led red
    for i in range(num_pixels):
        pixels[i] = ((percentage * 255), 0, 0)
    pixels.show()



    
def get_breaths_per_min(age):
    # returns the number of breaths per minute based on their age starting at age 4+.
    # source of breathing rate https://www.uptodate.com/contents/image/print?imageKey=EM%2F78097
    match age:
        case 4:
            return 25
        case 5:
            return 23
        case 6:
            return 21
        case 7:
            return 20
        case 8:
            return 19
        case 9:
            return 19
        case 10:
            return 18
        case _:
            return 18
             
def handle_button_press():
    global led_pattern
    global endLedEffect
    global ledThread
    print('button was pressed')

    # TODO update the led pattern to be an array/dictionary
    led_pattern = led_pattern + 1
    if led_pattern > 8:
        print('Restarting led count')
        led_pattern = 0
        endLedEffect = True
        ledThread.join()
        return

    print('Current Led Pattern:')
    print(led_pattern)
    if led_pattern == 1:
        tempThread = threading.Thread(target=ledRainbow)
    elif led_pattern == 2:
        tempThread = threading.Thread(target=ledFadeRed)
    elif led_pattern == 3:
        tempThread = threading.Thread(target=countingLed)
    elif led_pattern == 4:
        tempThread = threading.Thread(target=currentTime)
    elif led_pattern == 5:
        tempThread = threading.Thread(target=blueLightTrack)
    elif led_pattern == 6:
        tempThread = threading.Thread(target=redLightTrack)
    elif led_pattern == 7:
        tempThread = threading.Thread(target=greenLightTrack)
    elif led_pattern == 8:
        tempThread = threading.Thread(target=slowLedRainbow)

    try:
        print (ledThread)
    except UnboundLocalError:
        ledThread = tempThread
        
    while ledThread.is_alive():
        endLedEffect = True
        ledThread.join()
        time.sleep(1)
    ledThread = tempThread
    ledThread.start()

def handle_button_held():
    global led_pattern
    global endLedEffect
    print('button was Held')
    endLedEffect = True
    ledThread.join()
#    led_pattern = 0

# The amount of time you have to hold the button before it 
button.hold_time = 2 
button.when_held = handle_button_held
button.when_pressed = handle_button_press
print('WELCOME to LED CHRISTMAS SHOW')
print('press the button to start')
#blueLightTrack()
button.wait_for_press()
while True:
    time.sleep(0.1)
