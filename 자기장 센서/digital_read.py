import RPi.GPIO as GPIO
import time

#GPIO Mode Setting
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)

#Check PIN23 state every seconds
#Ctrl + C to Quit
while True:
    try:
        print(GPIO.input(23))
        time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()

