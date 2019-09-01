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

def magentic_state(door_open):
    door_open = GPIO.input(SENSOR_PIN)

    return door_open

def TimeCapture():
    while True :
        now = time.localtime()
        time_list = []
            
        now_hour = now.tm_hour
        if now_hour < 10:
            time_list.append(0)
            time_list.append(str(now_hour))
        else:
            time_list.append(str(now_hour/10))
            time_list.append(str(now_hour%10))
                    
        time_list.append("")
        time_list.append("")
                    
        now_min = now.tm_min
        if now_min < 10:
            time_list.append(0)
            time_list.append(str(now_min))
        else:
            time_list.append(str(now_min/10))
            time_list.append(str(now_min%10))
                    
        return time_list, now_hour, now_min



try:
    print("Press Ctrl+C to Exit\n")
    print("default door_state = {}".format(door_state))

    #While Statement that checks the door frequently
    time_list = [] 
    tmp =[]
    auto_close_flag = 0

    while(True):
        
        time_list, now_hour, now_min = TimeCapture()

        if tmp != time_list :
            tmp = time_list
            print("now time : %s%s-%s%s" %(tmp[0], tmp[1], tmp[4], tmp[5]))
        # when the time is 5:00 Am door state is closed
        if now_hour == 0 and now_min > 30:
            if auto_close_flag == 0:
                auto_close_flag = 1
                door_state = bool(0)
                firebase.put('/', "door_state", door_state)
        else:
            auto_close_flag = 0

        door_open = GPIO.input(SENSOR_PIN)
        
        if door_open == bool(1):
            door_state = bool(1)
            firebase.put('/', "door_state", door_state)

        
        time.sleep(CHECK_TIME)

#When Ctrl+C is pressed
except KeyboardInterrupt: 
    GPIO.remove_event_detect(SENSOR_PIN)
    GPIO.cleanup()

