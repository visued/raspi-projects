#!/usr/bin/python
import RPi.GPIO as GPIO
import time

#set pin sensor
sensor = 5

#set pin list
pinList = [2, 3, 4, 17, 27, 22, 10, 9]

#set time for sleep relay
SleepTimeL = 1

#set previous and current state sensor
previous_state = False
current_state = False

try:
	while True:
		#set board mode
		GPIO.setmode(GPIO.BCM)

		#set setup sensor
		GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)

		#loop in pin list and setup
		for i in pinList:
        		GPIO.setup(i, GPIO.OUT)
        		GPIO.output(i, GPIO.HIGH)
		#sleep 0.1 
		time.sleep(0.1)
		
	    	previous_state = current_state
	    	current_state = GPIO.input(sensor)
	    	if current_state != previous_state:
	        	new_state = "Move dectected!" if current_state else "No move, move to sensor for detect!"
	        	print("%s" % (new_state))
	        	if current_state:  # new
	                	GPIO.output(2, GPIO.LOW)
	                	print "Relay 1 active!"
	                	time.sleep(SleepTimeL);
	                	GPIO.output(3, GPIO.LOW)
	                	print "Relay 2 active!"
	                	time.sleep(SleepTimeL);
	                	GPIO.output(4, GPIO.LOW)
	                	print "Relay 3 active!"
	                	time.sleep(SleepTimeL);
	                	GPIO.output(17, GPIO.LOW)
	                	print "Relay 4 active!"
	                	time.sleep(SleepTimeL);
	                	GPIO.output(27, GPIO.LOW)
		                print "Relay 5 active!"
		                time.sleep(SleepTimeL);
	        	        GPIO.output(22, GPIO.LOW)
	                	print "Relay 6 active!"
		                time.sleep(SleepTimeL);
		                GPIO.output(10, GPIO.LOW)
	        	        print "Relay 7 active!"
	                	time.sleep(SleepTimeL);
		                GPIO.output(9, GPIO.LOW)
		                print "Relay 8 active!"
	        	        time.sleep(SleepTimeL);
except KeyboardInterrupt:
        print " Quit"

        #Reset GPIO settings
        GPIO.cleanup()

