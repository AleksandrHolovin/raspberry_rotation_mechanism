import RPi.GPIO as GPIO
import time
import termios
import tty
import sys
from pynput import keyboard

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

#setup
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setup(relay1_pin, GPIO.OUT)  
GPIO.setup(relay2_pin, GPIO.OUT)  
GPIO.setup(relay3_pin, GPIO.OUT)  
GPIO.setup(relay4_pin, GPIO.OUT)

GPIO.setup(relay5_pin, GPIO.OUT)
GPIO.setup(relay6_pin, GPIO.OUT)
GPIO.setup(relay7_pin, GPIO.OUT)
GPIO.setup(relay8_pin, GPIO.OUT)

GPIO.output(relay1_pin, True)
GPIO.output(relay2_pin, True)
GPIO.output(relay3_pin, True)
GPIO.output(relay4_pin, True)
GPIO.output(relay5_pin, True)
GPIO.output(relay6_pin, True)
GPIO.output(relay7_pin, True)
GPIO.output(relay8_pin, True)

def start_first_engine_in_direct_mode():
    GPIO.output(relay1_pin, False)
    GPIO.output(relay2_pin,False)
    GPIO.output(relay3_pin, True)
    GPIO.output(relay4_pin, True)

def start_first_engine_in_reverse_mode():
    GPIO.output(relay1_pin, True)
    GPIO.output(relay2_pin,True)
    GPIO.output(relay3_pin, False)
    GPIO.output(relay4_pin, False)

def stop_first_engine():
    GPIO.output(relay1_pin, True)
    GPIO.output(relay2_pin, True)
    GPIO.output(relay3_pin, True)
    GPIO.output(relay4_pin, True)

def start_second_engine_in_direct_mode():
    GPIO.output(relay5_pin, True)
    GPIO.output(relay6_pin, True)
    GPIO.output(relay7_pin, False)
    GPIO.output(relay8_pin, False)

def start_second_engine_in_reverse_mode():
    GPIO.output(relay5_pin, False)
    GPIO.output(relay6_pin, False)
    GPIO.output(relay7_pin, True)
    GPIO.output(relay8_pin, True)


def stop_second_engine():
    GPIO.output(relay5_pin, True)
    GPIO.output(relay6_pin, True)
    GPIO.output(relay7_pin, True)
    GPIO.output(relay8_pin, True)

def move_right():
    start_first_engine_in_direct_mode()
    start_second_engine_in_reverse_mode()

def move_left():
    start_first_engine_in_reverse_mode()
    start_second_engine_in_direct_mode()

def move_up():
    start_first_engine_in_direct_mode()
    start_second_engine_in_direct_mode()

def move_down():
    start_first_engine_in_reverse_mode()
    start_second_engine_in_reverse_mode()

def stop():
    stop_first_engine()
    stop_second_engine()

# Disable terminal echo
def disable_echo():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    return old_settings

# Restore terminal settings
def restore_echo(old_settings):
    fd = sys.stdin.fileno()
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

# Your key detection script
key_states = {
    'up': False,
    'down': False,
    'left': False,
    'right': False
}

def on_press(key):
    try:
        if key == keyboard.Key.up and not key_states['up']:
            key_states['up'] = True
            move_up()
            # print("key up pressed")
        elif key == keyboard.Key.down and not key_states['down']:
            key_states['down'] = True
            move_down()
            # print("key down pressed")
        elif key == keyboard.Key.left and not key_states['left']:
            key_states['left'] = True
            move_left()
            # print("key left pressed")
        elif key == keyboard.Key.right and not key_states['right']:
            key_states['right'] = True
            move_right()
            # print("key right pressed")
    except AttributeError:
        pass

def on_release(key):
    try:
        if key == keyboard.Key.up and key_states['up']:
            key_states['up'] = False
            stop()
            # print("key up released")
        elif key == keyboard.Key.down and key_states['down']:
            key_states['down'] = False
            stop()
            # print("key down released")
        elif key == keyboard.Key.left and key_states['left']:
            key_states['left'] = False
            stop()
            # print("key left released")
        elif key == keyboard.Key.right and key_states['right']:
            key_states['right'] = False
            stop()
            # print("key right released")
        
        if key == keyboard.Key.esc:
            return False  # Stop listener
    except AttributeError:
        pass

def main():
    old_settings = disable_echo()
    try:
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    finally:
        restore_echo(old_settings)
        GPIO.cleanup()  # Clean up GPIO settings

if __name__ == "__main__":
    main()




# # Main Loop
# try:
#     while True:
#         start_second_engine_in_direct_mode()
#         time.sleep(1)  # Relays on for 1 second
        
#         stop_second_engine()
#         time.sleep(1)  # Pause for 5 seconds

# except KeyboardInterrupt:
#     pass

# finally:  
#     GPIO.cleanup()  # Clean up GPIO settings
