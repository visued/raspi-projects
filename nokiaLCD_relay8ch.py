#!/usr/bin/python
import math
import time
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def lcdAtt(text):
        # Clear image buffer.
        draw.rectangle((0,0,84,48), outline=255, fill=255)
        draw.text((0, 0), text,font=font, fill=0)
        # Draw the image buffer.
        disp.image(image)
        disp.display()

# Raspberry Pi hardware SPI config:
SCLK = 17
DIN = 18
DC = 27
RST = 23
CS = 22
# Hardware SPI usage:
disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)
# Initialize library.
disp.begin(contrast=60)
# Clear display.
disp.clear()
disp.display()
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
# Load default font.
font = ImageFont.load_default()
# Load imagem to draw
draw = ImageDraw.Draw(image)

#set mode board
GPIO.setmode(GPIO.BCM)

#set GPIOS for use
pinList = [21, 20, 16, 12, 26, 19, 13, 6]

#loop setup GPIOS
for i in pinList:
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, GPIO.HIGH)
#time for active relay
SleepTimeL = 5

#main loop
try:
	GPIO.output(21, GPIO.LOW)
	lcdAtt("RL1 active!")
	time.sleep(SleepTimeL);
        GPIO.output(20, GPIO.LOW)
	lcdAtt("RL2 active!")
	time.sleep(SleepTimeL);
        GPIO.output(16, GPIO.LOW)
	lcdAtt("RL3 active!")
	time.sleep(SleepTimeL);
        GPIO.output(12, GPIO.LOW)
	lcdAtt("RL4 active!")
	time.sleep(SleepTimeL);
        GPIO.output(26, GPIO.LOW)
	lcdAtt("RL5 active!")
	time.sleep(SleepTimeL);
        GPIO.output(19, GPIO.LOW)
	lcdAtt("RL6 active!")
	time.sleep(SleepTimeL);
        GPIO.output(13, GPIO.LOW)
	lcdAtt("RL7 active!")
	time.sleep(SleepTimeL);
        GPIO.output(6, GPIO.LOW)
	lcdAtt("RL8 active!")
	time.sleep(SleepTimeL);
        lcdAtt("Fim, ate logo!")
        time.sleep(2)
        GPIO.cleanup()

#End program cleanly with keyboard
except KeyboardInterrupt:
        print " Quit"

        #Reset GPIO settings
        GPIO.cleanup()
