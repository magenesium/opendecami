import RPi.GPIO as GPIO
import time
from firebase import firebase

#CONST VARIABLES
SENSOR_PIN = 23
CHECK_TIME = 0.2

#GPIO Mode Setting
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

#Firebase Application Import
firebase = firebase.FirebaseApplication("https://door-decami.firebaseio.com/")
door_state = firebase.get('/door_state', None)

#Door Check Callback Function
def magnetic_callback(door_state):
    new_door_state = not bool(GPIO.input(SENSOR_PIN))
    if door_state != new_door_state:
        door_state = new_door_state
        print(door_state)
        firebase.put('/', "door_state", door_state)
    return door_state

try:
    print("Press Ctrl+C to Exit\n")
    print("default door_state = {}".format(door_state))

    #While Statement that checks the door frequently
    while(True): 
        door_state = magnetic_callback(door_state)
        time.sleep(CHECK_TIME)

#When Ctrl+C is pressed
except KeyboardInterrupt: 
    GPIO.remove_event_detect(SENSOR_PIN)
    GPIO.cleanup()

