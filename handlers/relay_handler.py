import RPi.GPIO as GPIO
import termios
import tty
import sys
import time
from handlers.elevation_handler import ElevationHandler

#pin definitions
#first engine pins
relay1_pin = 5 #GPIO 26 (Pin 37)
relay2_pin = 6 #GPIO 16 (Pin 36)
relay3_pin = 16 #GPIO 6 (Pin 31)
relay4_pin = 26 #GPIO 12 (Pin 31)

#second engine pins
relay5_pin = 17 #GPIO 17 (pin 11)
relay6_pin = 27 #GPIO 27 (pin 13)
relay7_pin = 22 #GPIO 22 (pin 15)
relay8_pin = 23 #GPIO 23 (pin 16)

relay_pins = [
    relay1_pin,
    relay2_pin,
    relay3_pin,
    relay4_pin,
    relay5_pin,
    relay6_pin,
    relay7_pin,
    relay8_pin,
]

#setup
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
#init pins and set default value
for pin in relay_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, True)
    
def handle_engines(ModeSet):
    for pin in ModeSet:
        GPIO.output(pin["pin"], pin["value"])
        
START_FIRST_ENGINE_IN_DIRECT_MODE_SET = [
    {
        "pin": relay1_pin,
        "value": False
    },
    {
        "pin": relay2_pin,
        "value": False
    },
    {
        "pin": relay3_pin,
        "value": True
    },
    {
        "pin": relay4_pin,
        "value": True
    }
]
START_FIRST_ENGINE_IN_REVERSE_MODE_SET = [
     {
        "pin": relay1_pin,
        "value": True
    },
    {
        "pin": relay2_pin,
        "value": True
    },
    {
        "pin": relay3_pin,
        "value": False
    },
    {
        "pin": relay4_pin,
        "value": False
    }
]

START_SECOND_ENGINE_IN_DIRECT_MODE_SET = [
     {
        "pin": relay5_pin,
        "value": True
    },
    {
        "pin": relay6_pin,
        "value": True
    },
    {
        "pin": relay7_pin,
        "value": False
    },
    {
        "pin": relay8_pin,
        "value": False
    }
]
START_SECOND_ENGINE_IN_REVERSE_MODE_SET = [
     {
        "pin": relay5_pin,
        "value": False
    },
    {
        "pin": relay6_pin,
        "value": False
    },
    {
        "pin": relay7_pin,
        "value": True
    },
    {
        "pin": relay8_pin,
        "value": True
    }
]

def move_right():
    handle_engines(START_FIRST_ENGINE_IN_DIRECT_MODE_SET)
    handle_engines(START_SECOND_ENGINE_IN_REVERSE_MODE_SET)

def move_left():
    handle_engines(START_FIRST_ENGINE_IN_REVERSE_MODE_SET)
    handle_engines(START_SECOND_ENGINE_IN_DIRECT_MODE_SET)

def move_up():
    handle_engines(START_FIRST_ENGINE_IN_DIRECT_MODE_SET)
    handle_engines(START_SECOND_ENGINE_IN_DIRECT_MODE_SET)

def move_down():
    handle_engines(START_FIRST_ENGINE_IN_REVERSE_MODE_SET)
    handle_engines(START_SECOND_ENGINE_IN_REVERSE_MODE_SET)

def stop():
    for pin in relay_pins:
        GPIO.output(pin, True)

# elevation_handler = ElevationHandler()
# elevation_handler.start()

def correct_elevation(target_angle, current_angle):
    if target_angle is None or current_angle is None:
        return
    
    listened_current_angle = elevation_handler.get_last_printed_angle()
    # Determine the difference
    angle_difference = target_angle - current_angle
    print(angle_difference)
    # Adjust to correct elevation angle
    if angle_difference > 0:
        move_up()
        while True:
            listened_current_angle = elevation_handler.get_last_printed_angle()
            
            # Stop the motor when the current angle reaches or exceeds the target angle
            if listened_current_angle >= target_angle:
                stop()
                break
            time.sleep(0.1) 
    elif angle_difference < 0:
        move_down()
        while True:
            listened_current_angle = elevation_handler.get_last_printed_angle()
            
            # Stop the motor when the current angle reaches or exceeds the target angle
            if listened_current_angle >= target_angle:
                stop()
                break
            time.sleep(0.1) 

