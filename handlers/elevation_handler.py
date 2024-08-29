# sensor_handler.py
import smbus
import time
import math
import threading

# MPU9250 I2C address
MPU9250_ADDRESS = 0x68

# MPU9250 Registers
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47
PWR_MGMT_1 = 0x6B

# Initialize the I2C bus
bus = smbus.SMBus(1)

# Wake up the MPU9250
bus.write_byte_data(MPU9250_ADDRESS, PWR_MGMT_1, 0x00)

def read_word(register):
    high = bus.read_byte_data(MPU9250_ADDRESS, register)
    low = bus.read_byte_data(MPU9250_ADDRESS, register + 1)
    value = (high << 8) + low
    return value

def read_word_2c(register):
    value = read_word(register)
    if value >= 0x8000:
        return -((65535 - value) + 1)
    else:
        return value

def get_accel_data():
    accel_x = read_word_2c(ACCEL_XOUT_H)
    accel_y = read_word_2c(ACCEL_YOUT_H)
    accel_z = read_word_2c(ACCEL_ZOUT_H)

    # Scale values to get G-forces
    accel_x = accel_x / 16384.0
    accel_y = accel_y / 16384.0
    accel_z = accel_z / 16384.0

    return accel_x, accel_y, accel_z

def get_elevation_angle(correction_factor=1.0):
    accel_x, accel_y, accel_z = get_accel_data()

    # Calculate elevation angle (pitch)
    elevation_angle = math.degrees(math.atan2(accel_x, math.sqrt(accel_y**2 + accel_z**2)))
    
    # Apply correction factor
    elevation_angle *= correction_factor
    
    # Round to nearest integer
    return int(round(elevation_angle))

def exponential_moving_average(current_value, previous_value, alpha=0.9):
    return int(round(alpha * current_value + (1 - alpha) * previous_value))

class ElevationHandler(threading.Thread):
    def __init__(self, alpha=0.9, correction_factor=1.05):
        threading.Thread.__init__(self)
        self.alpha = alpha
        self.correction_factor = correction_factor
        self.last_printed_angle = None
        self.smoothed_angle = get_elevation_angle(correction_factor)
        self.lock = threading.Lock()

    def run(self):
        while True:
            elevation_angle = get_elevation_angle(self.correction_factor)
            with self.lock:
                self.smoothed_angle = exponential_moving_average(elevation_angle, self.smoothed_angle, self.alpha)
                if self.smoothed_angle != self.last_printed_angle:
                    self.last_printed_angle = self.smoothed_angle
                    # print("Stabilized Elevation Angle (EMA): {}°".format(self.smoothed_angle))
            time.sleep(0.5)

    def get_last_printed_angle(self):
        with self.lock:
            return self.last_printed_angle
