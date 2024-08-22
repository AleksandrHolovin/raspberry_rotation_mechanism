import smbus
import time
import math

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

def get_gyro_data():
    gyro_x = read_word_2c(GYRO_XOUT_H)
    gyro_y = read_word_2c(GYRO_YOUT_H)
    gyro_z = read_word_2c(GYRO_ZOUT_H)

    # Scale values to degrees per second (dps)
    gyro_x = gyro_x / 131.0
    gyro_y = gyro_y / 131.0
    gyro_z = gyro_z / 131.0

    return gyro_x, gyro_y, gyro_z

def calibrate_gyro(samples=1000):
    print("Calibrating gyroscope... Keep the sensor still.")
    gyro_offset_x = 0
    gyro_offset_y = 0
    gyro_offset_z = 0

    for i in range(samples):
        gyro_x, gyro_y, gyro_z = get_gyro_data()
        gyro_offset_x += gyro_x
        gyro_offset_y += gyro_y
        gyro_offset_z += gyro_z
        time.sleep(0.01)  # Delay between readings

    gyro_offset_x /= samples
    gyro_offset_y /= samples
    gyro_offset_z /= samples

    print("Calibration complete.")
    print(f"Gyro Offsets -> X: {gyro_offset_x:.2f}, Y: {gyro_offset_y:.2f}, Z: {gyro_offset_z:.2f}")

    return gyro_offset_x, gyro_offset_y, gyro_offset_z

# Perform calibration
# gyro_offset_x, gyro_offset_y, gyro_offset_z = calibrate_gyro()
gyro_offset_x = -0.48
gyro_offset_y = -0.44
gyro_offset_z = -0.20

# Function to get calibrated gyro data
def get_calibrated_gyro_data():
    gyro_x, gyro_y, gyro_z = get_gyro_data()
    
    # Subtract the offsets
    gyro_x -= gyro_offset_x
    gyro_y -= gyro_offset_y
    gyro_z -= gyro_offset_z
    
    return gyro_x, gyro_y, gyro_z

# Function to calculate elevation angle (pitch) with correction factor
def get_elevation_angle(correction_factor=1.0):
    accel_x, accel_y, accel_z = get_accel_data()

    # Calculate elevation angle (pitch)
    elevation_angle = math.degrees(math.atan2(accel_x, math.sqrt(accel_y**2 + accel_z**2)))
    
    # Apply correction factor
    elevation_angle *= correction_factor
    
    # Round to nearest integer
    return int(round(elevation_angle))

# Function to apply an exponential moving average filter
def exponential_moving_average(current_value, previous_value, alpha=0.1):
    return int(round(alpha * current_value + (1 - alpha) * previous_value))

# Main loop to read and display stabilized elevation angle only when it changes
alpha = 0.5  # Smoothing factor; lower values smooth more
correction_factor = 1.05  # Adjust this to calibrate max angle to 90 degrees
smoothed_angle = get_elevation_angle(correction_factor)

last_printed_angle = smoothed_angle

while True:
    elevation_angle = get_elevation_angle(correction_factor)
    smoothed_angle = exponential_moving_average(elevation_angle, smoothed_angle, alpha)
    
    # Print only if the angle has changed
    if smoothed_angle != last_printed_angle:
        print("Stabilized Elevation Angle (EMA): {}°".format(smoothed_angle))
        last_printed_angle = smoothed_angle

    time.sleep(0.5)  # Small delay to avoid excessive CPU usage

