import RPi.GPIO as GPIO
import time
import threading

# GPIO pin assignments
CLK = 24  # Clock pin (connected to CLK on KY-040)
DT = 18   # Data pin (connected to DT on KY-040)

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Constants
STEPS_PER_REVOLUTION = 40  # Number of detents per revolution (adjust as needed)

class RotaryEncoderHandler(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.counter = 0
        self.angle = 0.0
        self.lock = threading.Lock()
        self.clkLastState = GPIO.input(CLK)

    def run(self):
        while True:
            clkState = GPIO.input(CLK)
            dtState = GPIO.input(DT)

            # Detect rotation
            if clkState != self.clkLastState:
                with self.lock:
                    if dtState != clkState:
                        self.counter += 1  # Clockwise rotation
                    else:
                        self.counter -= 1  # Counterclockwise rotation

                    # Calculate the angle
                    self.angle = (self.counter % STEPS_PER_REVOLUTION) * (360.0 / STEPS_PER_REVOLUTION)
                    
                # Uncomment the next line to print the angle within the thread (optional)
                # print(f"Angle: {self.angle:.2f} degrees")

            self.clkLastState = clkState

    def get_angle(self):
        with self.lock:
            return self.angle

